#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import glob
from typing import Any, Dict, List

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event: Any, context: Any) -> Dict[str, List[Dict[str, str]]]:
    """
    Creates a list with the .sql files contained in the folder "sql_create" 
    and returns it inside a dictionary.

    Args:
        event (Any): AWS Lambda event object. Not used in this function.
        context (Any): AWS Lambda context object. Not used in this function.

    Returns:
        dict: A dictionary containing a list of dictionaries with file names.
            Example:
            {
                "payload": [
                    {"file_name": "example_file1.sql"},
                    {"file_name": "example_file2.sql"},
                    # ... more file entries ...
                ]
            }

    Raises:
        Exception: If any error occurs during file retrieval.
    """
    try:
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Base path: {BASE_PATH}")

        files = glob.glob(f"{BASE_PATH}/sql_create/*.sql")
        files.sort()  # This is a must to execute views in the right order.

        logger.info(f"List of SQL files: {files}")

        payload = [{"file_name": f} for f in files]

        return {"payload": payload}

    except Exception as e:
        logger.error(f"Error in handler function: {str(e)}")
        raise e

if __name__ == '__main__':
    handler_return = handler(None, None)
    print(handler_return)