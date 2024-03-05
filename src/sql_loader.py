import os
import logging
import re
from typing import Any, Dict

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global variables
S3_BUCKET: str = os.getenv('aws_s3_data_lake')
S3_DATA_PATH: str = os.getenv('s3_data_path')
ATHENA_TARGET_DB: str = os.getenv('athena_target_db')
ATHENA_RAW_DB: str = os.getenv('athena_raw_db')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Reads a template SQL file, replaces placeholders, and returns the modified SQL query.

    Args:
        event (dict): The AWS Lambda event object.
        context (object): The AWS Lambda context object.

    Returns:
        dict: A dictionary containing 'query'.
    """

    logger.info(event)
    try:

        file_name = event.get('file_name')
        if not file_name:
            raise ValueError("File name not provided in the event.")

        tpl_str = open(file_name).read()

        # Remove SQL comments
        tpl_str = re.sub('^\s*--.*\n?', '', tpl_str, flags=re.MULTILINE)

        tpl_str = tpl_str.replace('{TARGET_DATABASE_TPL}', ATHENA_TARGET_DB)
        tpl_str = tpl_str.replace('{RAW_DATABASE}', ATHENA_RAW_DB)
        tpl_str = tpl_str.replace('{S3_TABLE_BASE_LOCATION_TPL}', f"{S3_BUCKET}/{S3_DATA_PATH}")
        tpl_str = tpl_str.replace('{DUMPDATE_P}', event.get('dumpdate', 'None'))

        logger.info(f"Processing file: {file_name}")

        return {
            "query": tpl_str
        }

    except Exception as e:
        logger.error(f"Error in handler function: {str(e)}")
        raise e
