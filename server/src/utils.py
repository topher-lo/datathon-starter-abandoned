"""Utility functions used in `streamlit-e2e-boilerplate`.
"""

import os
import re


def clean_text(text: str):
    """Returns string:
    1. Stripped of all whitespaces at start and end
    2. Any excess whitespace in between are replaced with an underscore "_"
    3. All characters are lowercased
    """
    clean_text = re.sub(' +', '_', text.strip()).lower()
    return clean_text


def make_path(path: str) -> str:
    """Make directory.
    Args:
        path (str): 
            Path to be made if it doesn't exist.
    Returns:
        path (str)
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


if __name__ == "__main__":
    pass
