import os
import pandas as pd
import logging
from bs4 import BeautifulSoup
import re

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

def get_prefix_suffix(word):
    """Returns the prefix and suffix of a word matching the regex."""
    match = KLIMA_PREFIX_SUFFIX.match(word)
    if match:
        return match.group(1) or "", match.group(2) or ""
    return "", ""

def extract_context_and_wordparts(words, context_window=3):
    """Extracts words with 'klima' and their context from the list of words."""
    matches = []
    for i, word in enumerate(words):
        if KLIMA_PART_MATCH.search(word):  # Match 'klima' or related words
            pre_context, post_context = get_context(words, i, context_window)
            prefix, suffix = get_prefix_suffix(word)
            matches.append({
                "pre_context": pre_context,
                "post_context": post_context,
                "prefix": prefix,
                "suffix": suffix,
            })
    return matches

def process_newspaper_with_context(newspaper, context_window=3):
    """Processes an individual newspaper file and returns a DataFrame."""
    html = read_html_file(newspaper['file_name'], newspaper['encoding'])
    bs = BeautifulSoup(html, "html.parser")
    body_text = bs.body.get_text(" ")
    words = body_text.split()
    matches_with_context = extract_context_and_wordparts(words, context_window)

    if matches_with_context:
        data = pd.DataFrame(matches_with_context)
    else:
        data = pd.DataFrame(columns=["pre_context", "post_context", "prefix", "suffix"])

    data["newspaper"] = newspaper["name"]
    data["date_published"] = newspaper["date"]
    return data
