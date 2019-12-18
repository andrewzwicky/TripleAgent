import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def execute_single_notebook(notebook_filename):
    with open(notebook_filename, "r", encoding="utf-8") as file_in:
        notebook = nbformat.read(file_in, as_version=4)

    preprocessor = ExecutePreprocessor(timeout=600, kernel_name="python3")

    preprocessor.preprocess(notebook, dict())

    with open(notebook_filename, "w", encoding="utf-8") as file_out:
        nbformat.write(notebook, file_out)
