"""This module contains utility functions.
"""

import re

from argparse import ArgumentTypeError

# The APA delimiters.

APA_DELIM_LIST: list[str] = [
    r'\.', r'\;', r'\?', r'\:', r'\—'
]

# The APA delimiter regex.
APA_DELIM_REGEX = re.compile(rf'([^{"".join(APA_DELIM_LIST)}]+[{"".join(APA_DELIM_LIST)}]?)\s*')

# The APA minor word list.
APA_MINOR_WORD_LIST = [
    'and', 'as', 'but', 'for', 'if', 'nor', 'or', 'so', 'yet', 'a', 'an',
    'the', 'as', 'at', 'by', 'in', 'of', 'off', 'on', 'per', 'to', 'up', 'via'
]

# The APA minor word regex.
APA_MINOR_WORDS_REGEX = re.compile(
    rf'(?!^)(?:(?<=\w[\'’])s|(?<=\s)(?:{r"|".join(APA_MINOR_WORD_LIST)}[.:;?—]))',
    re.IGNORECASE
)

# The list of metadata.
METADATA_LIST: list[str] = [
    'dc:identifier',
    'dc:title',
    'dc:language',
    'dc:contributor',
    'dc:creator',
    'dc:date',
    'dc:subject',
    'dc:type'
]


def clean_white_spaces(text: str) -> str:
    """Cleans a given text from white spaces.
    
    Args:
        text (str): the text to clean

    Returns:
        str: the cleaned text
    """
    return re.sub(r'\s+', ' ', text.strip())


def apa_title(text: str) -> str:
    """Return a copy of the string converted in apa_title.

    More specifically, the title case used is the APA style, where major words
    start with upper-cased characters and all remaining are lower-cased, except
    for minor words (e.g., and, the, of, etc.) where the whole
    word is lower-cased.

    Exceptions when minor words start with upper-cased character are:
     - at the start of the string
     - after punctuation (., :, ;, etc.)

    Args:
        text (str): the string to convert in apa_title

    Returns:
        str: the apa_titled string
    """
    text = text.title().strip()
    subtext_list = APA_DELIM_REGEX.findall(text)

    title = []
    for subtext in subtext_list:
        # lower all the minor words that are not at the start
        title.append(APA_MINOR_WORDS_REGEX.sub(lambda match: match[0].lower(), subtext))

    return ' '.join(title)


_SELECTOR_REGEX = re.compile(r'(\w*)\.?([\w\-_]*)')


def parse_selector(text: str) -> dict[str, str]:
    """Parse a selector in the form [tag].class.

    Args:
        text (str): the text to parse

    Raises:
        ArgumentTypeError: if the text is not a valid selector

    Returns:
        dict[str, str]: the parsed text
    """
    match = _SELECTOR_REGEX.match(text)

    if not match:
        raise ArgumentTypeError(f'{text} is invalid, must be [tag].class')

    return {'tag': match[1] or None, 'class': match[2] or None}
