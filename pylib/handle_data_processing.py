import os
import logging
import re
from bs4 import BeautifulSoup
import multiprocessing
from handle_sqlite import save_dataframe_to_db
import pandas as pd


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Regex patterns for 'klima'
KLIMA_PREFIX_SUFFIX = re.compile(r"(.*?)-?klima(?:-?(\w+))?", re.IGNORECASE)
KLIMA_PART_MATCH = re.compile(r"\bklima(?:\w+|-?\w+)?\b", re.IGNORECASE)


def read_html_file(filename, encoding="utf-8"):
    """Reads the HTML file content after normalizing the file path."""
    filename = os.path.normpath(filename)
    with open(filename, "r", encoding=encoding) as f:
        return f.read()


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
        lang = html_tag.get("lang", "") if html_tag else ""
        if not lang.startswith("de"):
            logging.info(f"Skipping {name} ({date}) due to non-German language: {lang}")
            return None, None

        # Extract the body first to reduce unnecessary processing
        body = bs.body
        if not body:
            logging.warning(f"No body content found in {name} ({date}).")

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
    """Processes newspapers in batches and saves results to DB with multiprocessing."""
    metadata_collection = []
    context_collection = []
    newspaper_id_counter = 1

    pool = multiprocessing.Pool(num_workers)

    for i in range(0, len(newspapers), batch_size):
        batch = newspapers[i : i + batch_size]  # Get the next batch

        results = pool.starmap(
            process_newspaper_wrapper, [(news, input_path_prefix) for news in batch]
        )

        for metadata, context_data in results:
            if metadata is None:
                continue

            metadata["newspaper_id"] = newspaper_id_counter
            metadata_collection.append(metadata)

            if metadata["klima_mentions_count"] > 0:
                for context in context_data:
                    context["newspaper_id"] = newspaper_id_counter
                context_collection.extend(context_data)

            newspaper_id_counter += 1

        # Convert batch to DataFrame and save
        if metadata_collection:
            logging.info(
                f"Processing at date {metadata_collection[-1].get("data_published", "Unknown Date")}."
            )
            final_metadata_df = pd.DataFrame(metadata_collection)
            save_dataframe_to_db(
                final_metadata_df, "newspapers", db_path=db_path, if_exists="append"
            )
            metadata_collection.clear()

        if context_collection:
            final_context_df = pd.DataFrame(context_collection)
            save_dataframe_to_db(
                final_context_df, "context", db_path=db_path, if_exists="append"
            )
            context_collection.clear()

    pool.close()
    pool.join()
