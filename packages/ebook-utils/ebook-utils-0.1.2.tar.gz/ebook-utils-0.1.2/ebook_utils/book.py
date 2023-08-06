"""This is a module that manages books.
"""

import sys
from dataclasses import dataclass

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from ebooklib.epub import EpubBook, EpubHtml

from ebook_utils.utils import METADATA_LIST, parse_selector, apa_title, clean_white_spaces


@dataclass
class TocNavPoint:
    text: str
    src: str


class Chapter:
    __title: str
    __contents: str
    __word_list: list[str]

    def __init__(self, title: str, contents: str):
        self.__title = title
        self.__contents = contents
        self.__word_list = clean_white_spaces(contents).split()

    @property
    def title(self) -> str:
        """Returns the title of the chapter."""
        return self.__title

    @property
    def contents(self) -> str:
        """Returns the contents of the chapter."""
        return self.__contents

    @property
    def num_words(self) -> int:
        """Returns the number of words of the chapter."""
        return len(self.__word_list)

    @property
    def num_pages(self) -> float:
        """Returns the approximate number of page of the chapter.

        It approximates the number of pages with an average of words per page.
        """
        return self.num_words / Book.AVG_WORDS_PER_PAGE

    def __repr__(self) -> str:
        return f'Chapter({repr(self.title)})'

    def __str__(self):
        return f'{self.title}'


class Book:
    # The average words per page.
    AVG_WORDS_PER_PAGE: int = 450

    # The epub object.
    __epub: EpubBook = None

    # The options passed on creation.
    __options: dict[str, any] = dict()

    # The book document list.
    __document_list: list[EpubHtml] = []

    # The chapter list.
    # TODO: should differentiate between chapter list and document list.
    __chapter_list: list[Chapter] = []

    # The TOC data info.
    __toc: list[TocNavPoint] = None

    def __init__(self, epub_file: str, options: dict[str, any]) -> None:
        self.__epub = epub.read_epub(epub_file)
        self.__options = options

        for document in self.__epub.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            self.__document_list.append(document)

            body_html: BeautifulSoup = BeautifulSoup(
                document.get_body_content(), 'lxml')
            doc_contents: str = body_html.get_text()

            if 'filter' in options and options['filter']:
                selector = parse_selector(options['filter'])
                chapter_html = body_html.find_all(
                    selector['tag'], class_=selector['class'])

                if len(chapter_html) > 0:
                    chapter_title = apa_title(chapter_html[0].get_text())
                    self.add_chapter(chapter_title, doc_contents)
            else:
                # if no filters, use each document as chapter
                self.add_chapter(document.file_name, doc_contents)

    def add_chapter(self, title: str, contents: str) -> None:
        """Adds a chapter in the book.

        Args:
            title (str): the chapter's title
            contents (str): the chapter's contents
        """
        chapter = Chapter(title, contents)
        self.__chapter_list.append(chapter)

    def get_metadata(self, attribute: str) -> list:
        """Returns the metadata from a given attribute.

        Args:
            attribute (str): the metadata attribute

        Returns:
            str: The metadata from the attribute
        """
        if attribute not in METADATA_LIST:
            print(
                f'{attribute} is not a valid metadata. See --metadata-list for valid metadata.', file=sys.stderr)
            sys.exit()

        [namespace, name] = attribute.split(':')
        return [m[0] for m in self.__epub.get_metadata(namespace.upper(), name)]

    def get_chapters_from_toc(self) -> list[Chapter]:
        """Returns the chapter list from the table of contents."""
        chapters: list[Chapter] = []

        for toc_nav_point in self.toc:
            item: EpubHtml = self.__epub.get_item_with_href(toc_nav_point.src)
            contents = BeautifulSoup(item.get_body_content(), 'lxml').text
            chapters.append(Chapter(toc_nav_point.text, contents))

        return chapters

    @property
    def toc(self) -> list[TocNavPoint]:
        """Returns the list of contents of the book."""
        if not self.__toc:
            self.__toc = []

            # get the TOC navigation document file
            toc_document = next(
                self.__epub.get_items_of_type(ebooklib.ITEM_NAVIGATION))

            if toc_document:
                toc_xml = BeautifulSoup(toc_document.get_content(), 'lxml')
                for navpoint in toc_xml.navmap.find_all('navpoint'):
                    toc_nav_point = TocNavPoint(
                        apa_title(navpoint.navlabel.text.strip()), navpoint.content["src"])
                    self.__toc.append(toc_nav_point)

        return self.__toc

    @property
    def identifiers(self) -> list[str]:
        """Return the list of identifier of the book."""
        return self.get_metadata('dc:identifier')

    @property
    def titles(self) -> list[str]:
        """Returns the list of titles of the book."""
        return self.get_metadata('dc:title')

    @property
    def languages(self) -> list[str]:
        """Returns the list of languages of the book."""
        return self.get_metadata('dc:language')

    @property
    def creators(self) -> list[str]:
        """Returns the list of creators of the book."""
        return self.get_metadata('dc:creator')

    @property
    def document_list(self) -> list[EpubHtml]:
        """Returns a copy of the book's documents."""
        return self.__document_list.copy()

    @property
    def chapter_list(self) -> list[Chapter]:
        """Returns a copy of the book's chapter list."""
        return self.__chapter_list.copy()

    @property
    def options(self) -> dict[str, any]:
        """Returns the dictionary of options."""
        return self.__options.copy()

    def __getitem__(self, pos):
        return self.chapter_list[pos]

    def __iter__(self):
        return iter(self.chapter_list)

    def __repr__(self) -> str:
        return f'Book({repr(self.titles[0])}, {repr(self.creators[0])})'

    def __str__(self):
        return f'{self.titles[0]}, {self.creators[0]}'
