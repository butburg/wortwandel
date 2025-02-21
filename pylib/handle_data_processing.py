import os
import logging
import re
from bs4 import BeautifulSoup


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Regex patterns for 'klima'
KLIMA_PREFIX_SUFFIX = re.compile(r'(.*?)-?klima(?:-?(\w+))?', re.IGNORECASE)
KLIMA_PART_MATCH = re.compile(r'\bklima(?:\w+|-?\w+)?\b', re.IGNORECASE)


def read_html_file(filename, encoding="utf-8"):
    """Reads the HTML file content after normalizing the file path."""
    filename = os.path.normpath(filename)  # Normalize the path
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
            matches.append({
                "pre_context": pre_context,
                "post_context": post_context,
                "prefix": prefix,
                "suffix": suffix,
            })
    return matches


def process_newspaper_with_context(newspaper, context_window=3):
    """Processes an individual newspaper file and returns dictionaries for context and metadata."""

    logging.info(f"Processing newspaper: {newspaper['name']} ({newspaper['date']})")

    try:
        # Read and parse the html file
        html = read_html_file(newspaper['file_name'], newspaper['encoding'])
        bs = BeautifulSoup(html, "html.parser")
        body_text = bs.body.get_text(" ")
        words = body_text.split()

        # Extracts context, prefix, and suffix for each 'klima' mention found in the newspaper's content.
        klima_contexts = extract_context_and_wordparts(words, context_window)

        # Prepare metadata, so we also know, if there is no 'klima' at all in a newspaper
        metadata = {
            "newspaper": newspaper["name"],
            "data_published": newspaper["date"],
            "klima_mentions_count": len(klima_contexts)
            }

        # Log the result of this newspaper and the count of substring 'klima'
        if metadata['klima_mentions_count'] == 0:
            logging.info(f"No 'klima' mentions found in {newspaper['name']} for {newspaper['date']}.")
        else:
            logging.info(f"{metadata['klima_mentions_count']} 'klima' mentions in {newspaper['name']} for {newspaper['date']}.")


        return metadata, klima_contexts

    except Exception as e:
        logging.error(f"Error processing {newspaper['name']}: {e}")
        raise
