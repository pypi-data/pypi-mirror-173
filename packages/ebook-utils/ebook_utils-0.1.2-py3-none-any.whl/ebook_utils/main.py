import sys
from argparse import ArgumentParser, Namespace
from typing import Optional, TextIO


from ebook_utils._version import __version__
from ebook_utils.book import Book
from ebook_utils.utils import METADATA_LIST

# the output file
output_file: TextIO

# the book
book: Book


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='ebook-utils',
        description='A simple ebook utility program.'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s v' + __version__
    )

    parser.add_argument(
        '-i', '--input',
        required=False,
        help='the input file'
    )

    epub_actions = parser.add_mutually_exclusive_group()

    epub_actions.add_argument(
        '-w', '--word-count',
        action='store_true',
        help='print the word count of each selected document'
    )

    epub_actions.add_argument(
        '-W', '--word-count-total',
        action='store_true',
        help='print the total word count'
    )

    epub_actions.add_argument(
        '-m', '--metadata',
        help='print a metadata for an epub'
    )

    epub_actions.add_argument(
        '-d', '--document-list',
        action='store_true',
        help='print the documents in the epub'
    )

    parser.add_argument(
        '-t', '--toc',
        action='store_true',
        help='uses the book\'s table of contents'
    )

    parser.add_argument(
        '-f', '--filter',
        help='the document filter selector (CSS-like)'
    )

    parser.add_argument(
        '-M', '--metadata-list',
        action='store_true',
        help='print the list of epub metadata'
    )

    parser.add_argument(
        '-o', '--output',
        required=False,
        help='the output file'
    )

    return parser


def get_output_file(output_path: Optional[str] = None) -> TextIO:
    """Returns the output file from a given string or the standard output if
    no output is passed.

    Args:
        output_path (str): the output path

    Returns:
        TextIO: the output file
    """
    file: TextIO = sys.stdout

    if output_path:
        try:
            file = open(output_path, 'w')
        except IOError as error:
            print(error, file=sys.stderr)
            sys.exit()

    return file


def exec_word_count_command(table_of_contents: bool, count_total: bool) -> None:
    """Executes the word count command on the given book.

    Args:
        table_of_contents (bool): if the word count must be computed on the
                                  table of contents.
        count_total (bool): to output the total count of words
    """
    chapter_list = list(iter(book))

    if table_of_contents:
        chapter_list = book.get_chapters_from_toc()

    num_words_total: int = 0
    for chapter in chapter_list:
        num_words_total += chapter.num_words

        if not count_total:
            print(f'{chapter.title},{chapter.num_words}', file=output_file)

    if count_total:
        print(f'num_chapters={len(chapter_list)}')
        print(f'num_words_total={num_words_total}')


def exec_metadata_command(attr: str) -> None:
    """Executes the metadata command on the given book.

    Args:
        attr (str): the metadata attribute (e.g., dc:title)
    """
    metadata_list: list[str] = book.get_metadata(attr)
    print('\n'.join(metadata_list), file=output_file)


def exec_toc_command() -> None:
    """Executes the TOC command on the given book."""
    for toc_nav_point in book.toc:
        print(f'{toc_nav_point.text} ("{toc_nav_point.src}")', file=output_file)


def exec_document_list_command() -> None:
    """Executes the document list command on the given book."""
    for document in book.document_list:
        print(f'{document.get_name()} (#{document.get_id()})', file=output_file)


def exec_default_epub_command() -> None:
    """Executes the default command for the given book."""
    print(f'titles={book.titles}', file=output_file)
    print(f'creators={book.creators}', file=output_file)
    print(f'identifiers={book.identifiers}', file=output_file)
    print(f'languages={book.languages}', file=output_file)
    print(f'documents={len(book.chapter_list)}', file=output_file)
    print(f'doc_filter={book.options["filter"]}', file=output_file)


def epub_commands(args: Namespace) -> None:
    """Executes commands related to an epub.

    Args:
        args: the given arguments
    """
    global output_file
    output_file = get_output_file(args.output)

    if args.word_count or args.word_count_total:
        exec_word_count_command(args.toc, args.word_count_total)
    elif args.metadata:
        exec_metadata_command(args.metadata)
    elif args.toc:
        exec_toc_command()
    elif args.document_list:
        exec_document_list_command()
    else:
        exec_default_epub_command()

    output_file.close()


def generic_commands(args: Namespace) -> None:
    """Executes generic commands that do not involve an epub.

    Args:
        args: the given arguments
    """
    if args.metadata_list:
        print('\n'.join(METADATA_LIST))


def main(args: list[str] = None) -> int:
    parser: ArgumentParser = create_parser()
    args: Namespace = parser.parse_args(args)

    if len(sys.argv) == 1:
        parser.print_usage()
    elif args.input:
        global book
        options: dict[str, str] = {'filter': args.filter}
        book = Book(args.input, options)
        epub_commands(args)
    else:
        generic_commands(args)

    return 0


if __name__ == '__main__':
    exit(main())
