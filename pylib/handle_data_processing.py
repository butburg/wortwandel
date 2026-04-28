import os
import logging
import re
from bs4 import BeautifulSoup, Tag
import multiprocessing
from handle_sqlite import (
    get_db_connection,
    initialize_dwh_schema,
    upsert_newspaper,
    insert_context_rows,
)


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Regex patterns for 'klima'
KLIMA_PREFIX_SUFFIX = re.compile(r"(.*?)-?klima(?:-?(\w+))?", re.IGNORECASE)
KLIMA_PART_MATCH = re.compile(r"\bklima(?:\w+|-?\w+)?\b", re.IGNORECASE)


def read_html_file(filename, encoding="utf-8", fallback_encodings=("cp1252", "latin1")):
    """Reads the HTML file content after normalizing the file path."""
    filename = os.path.normpath(filename)
    with open(filename, "rb") as f:
        raw = f.read()

    encodings = []
    if encoding:
        encodings.append(encoding)
    for fallback_encoding in fallback_encodings:
        if fallback_encoding and fallback_encoding not in encodings:
            encodings.append(fallback_encoding)

    for current_encoding in encodings:
        try:
            text = raw.decode(current_encoding)
            if current_encoding != encoding:
                logging.info(
                    "Decoded %s with fallback encoding %s after %s failed.",
                    filename,
                    current_encoding,
                    encoding,
                )
            return text
        except UnicodeDecodeError as exc:
            bad_byte = raw[exc.start] if exc.start < len(raw) else None
            if bad_byte is not None:
                logging.warning(
                    "Failed to decode %s with %s at byte 0x%02x (offset %s); retrying.",
                    filename,
                    current_encoding,
                    bad_byte,
                    exc.start,
                )
            else:
                logging.warning(
                    "Failed to decode %s with %s at offset %s; retrying.",
                    filename,
                    current_encoding,
                    exc.start,
                )

    logging.warning(
        "Falling back to replacement decoding for %s after encodings failed: %s",
        filename,
        ", ".join(encodings) or encoding or "utf-8",
    )
    return raw.decode(encoding or "utf-8", errors="replace")


def get_context(words, index, context_window=3):
    """Returns the pre-context and post-context for a word."""
    pre_context = words[max(0, index - context_window) : index]
    post_context = words[index + 1 : index + 1 + context_window]
    return " ".join(pre_context), " ".join(post_context)


def extract_prefix_suffix(word):
    """Extracts and returns the prefix and suffix of a word matching the 'klima' regex pattern."""
    match = KLIMA_PREFIX_SUFFIX.match(word)
    if match:
        return match.group(1) or "", match.group(2) or ""
    return "", ""


def extract_context_and_wordparts(words, context_window=3):
    """Extracts context, prefix, and suffix for each 'klima' mention found in the list of words."""
    matches = []
    for i, word in enumerate(words):
        if KLIMA_PART_MATCH.search(word):  # Match 'klima' or related words
            pre_context, post_context = get_context(words, i, context_window)
            prefix, suffix = extract_prefix_suffix(word)
            matches.append(
                {
                    "pre_context": pre_context,
                    "post_context": post_context,
                    "prefix": prefix,
                    "suffix": suffix,
                }
            )
    return matches


def process_newspaper_with_context(name, date, file_path, encoding, context_window=3):
    """Processes an individual newspaper file and returns dictionaries for context and metadata."""
    try:
        # Read and parse the html file
        html = read_html_file(file_path, encoding)

        # Parse only with lxml for performance
        bs = BeautifulSoup(html, "lxml")

        # clear non de entries before by checking in in <html lang="...">
        # all accesible website own a lang tag
        html_tag = bs.find("html")
        lang = ""
        if isinstance(html_tag, Tag):
            lang_attr = html_tag.get("lang", "")
            if isinstance(lang_attr, list):
                lang = str(lang_attr[0]) if lang_attr else ""
            else:
                lang = str(lang_attr)

        if not lang.startswith("de"):
            logging.info(f"Skipping {name} ({date}) due to non-German language: {lang}")
            return None, None

        # Extract the body first to reduce unnecessary processing
        body = bs.body
        words = []
        if not body:
            logging.warning(f"No body content found in {name} ({date}).")
        else:
            # Remove unwanted elements (script, style, etc.) to minimize processing
            for tag in body(["script", "style", "noscript", "iframe", "meta", "link"]):
                tag.decompose()  # Deletes tag and contents to save memory

            # Extract words efficiently. Format of stripped_string are phrases, splitting them to get words/token
            words = [word for text in body.stripped_strings for word in text.split()]

        # Extracts context, prefix, and suffix for each 'klima' mention found in the newspaper's content.
        klima_contexts = extract_context_and_wordparts(words, context_window)

        # Prepare metadata, so we also know, if there is no 'klima' at all in a newspaper
        metadata = {
            "newspaper_name": name,
            "data_published": date,
            "klima_mentions_count": len(klima_contexts),
        }

        # logging.info(f"{metadata['klima_mentions_count']} 'klima' mentions in {name} for {date}.")

        return metadata, klima_contexts

    except Exception as e:
        logging.error(f"Error processing {name}: {e}")
        raise


def process_newspaper_wrapper(news, input_path_prefix):
    """Wrapper function to process a single newspaper and catch errors."""
    try:
        news["file_path"] = f"{input_path_prefix}/{news.pop('file_name')}"
        return process_newspaper_with_context(**news)
    except Exception as e:
        logging.error(
            f"Error processing newspaper {news['name']} ({news['date']}): {e}"
        )
        return None, None  # Return None to indicate failure


def batch_process_newspapers(
    newspapers,
    batch_size=2,
    num_workers=4,
    db_path="data_output/dwh_data.db",
    input_path_prefix="data_input",
):
    """Processes newspapers in batches and saves results to DB idempotently."""

    pool = multiprocessing.Pool(num_workers)
    connection = get_db_connection(db_path)
    cursor = connection.cursor()
    initialize_dwh_schema(connection)

    try:
        for i in range(0, len(newspapers), batch_size):
            batch = newspapers[i : i + batch_size]  # Get the next batch

            results = pool.starmap(
                process_newspaper_wrapper, [(news, input_path_prefix) for news in batch]
            )

            last_date = "Unknown Date"
            inserted_context_rows = 0
            upserted_newspapers = 0

            for metadata, context_data in results:
                if metadata is None:
                    continue

                last_date = metadata.get("data_published", "Unknown Date")
                newspaper_id, was_inserted = upsert_newspaper(
                    cursor,
                    metadata.get("newspaper_name", ""),
                    metadata.get("data_published", ""),
                    metadata.get("klima_mentions_count", 0),
                )
                upserted_newspapers += 1

                # Import context only for newly inserted newspaper-day rows.
                # Existing rows are considered already imported and are skipped.
                if was_inserted and metadata.get("klima_mentions_count", 0) > 0:
                    inserted_context_rows += insert_context_rows(
                        cursor, newspaper_id, context_data or []
                    )

            connection.commit()
            if upserted_newspapers > 0:
                logging.info(
                    "Processed batch up to %s: %s newspapers upserted, %s new context rows inserted.",
                    last_date,
                    upserted_newspapers,
                    inserted_context_rows,
                )
    finally:
        pool.close()
        pool.join()
        cursor.close()
        connection.close()
