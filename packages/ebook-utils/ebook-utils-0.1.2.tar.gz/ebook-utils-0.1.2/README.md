# ebook-utils

A simple ebook utility program made in Python.

```
usage: ebook-utils [-h] [-v] [-i INPUT] [-w | -W | -t | -m METADATA] [-f FILTER] [--metadata-list] [-o OUTPUT]
```

## Installation

To install and use the package, you can use `pip`. First clone the package into your system and then install it

```sh
cd ebook-utils/
pip install .
```

Then you can use `ebook-utils` in your terminal.

## Contributing

If you want to contribute, fork the repository and then clone it into your system. After that, create a virtual
environment and activate it

```sh
cd ebook-utils/
python -m venv venv
source env/bin/activate
```

Install all the package requirements by running

```sh
make init
```

Finally, you install the package with

```sh
pip install -e .
```

Then make your edits, commit, and create a merge request!

## Example

```sh
ebook-utils -wf .myclass -i myebook.epub
```

## Authors

Michele Lapolla

## License

This project is licensed under the GNU GPLv3 License — see `LICENSE` for details.
