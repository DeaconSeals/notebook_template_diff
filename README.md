# MEGADIFF

## Dependencies
`pip install jupytext`

Only looks at `.py` and `.ipynb` files.

## Usage
`python megadiff.py /path/to/template/directory/ /path/to/directories/i/want/to/diff/*`

Populates a `diff/` directory in the calling directory with files containing text not found in the template directory and adhering to the file structure of the template directories.