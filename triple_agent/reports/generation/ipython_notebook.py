import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def execute_single_notebook(notebook_filename):
    with open(notebook_filename, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

    ep.preprocess(nb, dict())

    with open(notebook_filename, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
