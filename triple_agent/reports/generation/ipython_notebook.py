import os
import logging

logger = logging.getLogger("triple_agent")


def execute_single_notebook(notebook_filename):
    logger.info("executing %s", notebook_filename)
    os.system(
        f'jupyter nbconvert --to notebook --execute --inplace "{notebook_filename}" --log-level WARN'
    )
