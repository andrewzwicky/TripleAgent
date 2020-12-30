import sys
import asyncio

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


def execute_single_notebook(notebook_filename):
    # See https://bugs.python.org/issue37373 :(
    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with open(notebook_filename, "r", encoding="utf-8") as file_in:
        notebook = nbformat.read(file_in, as_version=4)

    preprocessor = ExecutePreprocessor(timeout=600, kernel_name="python3")

    preprocessor.preprocess(notebook, dict())

    with open(notebook_filename, "w", encoding="utf-8") as file_out:
        nbformat.write(notebook, file_out)
