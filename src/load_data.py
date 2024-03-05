#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import glob
import json
from datetime import date, timedelta, datetime
from typing import Dict, Any, Generator

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Global variables
DAYS_BACK = 0 # Number of days needed to go back to read data TODO move to env

def generate_date_range(start: date, end: date, interval: int) -> Generator[date, None, None]:
    """
    Generates a range of dates between a start and end date with a specified interval.

    Args:
        start (date): The starting date of the range.
        end (date): The ending date of the range.
        interval (int): The interval between consecutive dates.

    Yields:
        date: The generated dates within the specified range.

    Example:
        Example of using the date_range function.
        >>> for dt in date_range(date(2022, 1, 1), date(2022, 1, 10), 2):
        ...     print(dt)
        2022-01-01
        2022-01-03
        2022-01-05
        2022-01-07
        2022-01-09
    """
    diff = (end - start) / interval
    for i in range(diff.days + 1):
        yield start + timedelta(interval) * i


def generate_script_info(file_name: str, execution_date: date) -> Dict[str, Any]:
    """
    Generates a dictionary with information about the executed SQL script.

    Args:
        file_name (str): The name of the SQL script file.
        execution_date (date): The date when the script was executed.

    Returns:
        dict: A dictionary containing script information.
            - 'file_name' (str): The name of the SQL script file.
            - 'dumpdate' (str): The formatted execution date in 'YYYYMMDD' string.
            - 'year' (str): The year extracted from the execution date.
            - 'month' (str): The month extracted from the execution date.
            - 'day' (str): The day extracted from the execution date.

    Example:
        Example of using the generate_script_info function.
        >>> generate_script_info('example.sql', date(2022, 1, 1))
        {'file_name': 'example.sql', 'dumpdate': '2022-01-01', 'year': '2022', 'month': '1', 'day': '1'}
    """
    return {
        'file_name': file_name,
        'dumpdate': execution_date.strftime('%Y%m%d'),
        'year': str(execution_date.year),
        'month': str(execution_date.month),
        'day': str(execution_date.day),
    }


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handles the execution of SQL scripts based on the provided event parameters.

    Args:
        event (dict): A dictionary containing parameters for controlling script execution.
            - 'history' (str): If 'true', indicates a historical data load.
            - 'start_date' (str): Start date for historical data load in 'YYYY-MM-DD' format.
            - 'end_date' (str, optional): End date for historical data load in 'YYYY-MM-DD' format.

        context: AWS Lambda context object.

    Returns:
        dict: A dictionary containing the executed SQL script details.
            - 'payload' (list): List of dictionaries with details for each executed script.
                Each dictionary contains:
                - 'script_name' (str): Name of the executed SQL script.
                - 'execution_date' (str): Date when the script was executed.

    Raises:
        Exception: If any error occurs during script execution.

    Example:
        Example of handling an event to execute SQL scripts.
        >>> event = {
        ...     'history': 'true',
        ...     'start_date': '2022-01-01',
        ...     'end_date': '2022-01-31',
        ...     'file': 'specific_script'
        ... }
        >>> handler(event, context)
        {'payload': [{'script_name': 'specific_script.sql', 'execution_date': '2022-01-01'}, ...]}
    """
    logger.info(f"### EVENT: {event}")

    is_history = False
    dates = []

    try:
        this_is_the_day = (datetime.now() - timedelta(DAYS_BACK)).date()

        BASE_PATH = os.path.dirname(os.path.abspath(__file__)).rstrip('/')
        logger.info(BASE_PATH)

        files = glob.glob(f"{BASE_PATH}/sql_load/*.sql")
        files.sort() # This is a must to execute views in the right order.

        logger.info(files)

        if 'history' in event and event['history'] == 'true' and 'start_date' in event:
            is_history = True
            start_date = datetime.strptime(event['start_date'], '%Y-%m-%d').date()

            if 'end_date' in event:
                end_date = datetime.strptime(event['end_date'], '%Y-%m-%d').date()
            else:
                end_date = this_is_the_day

            dates = list(generate_date_range(start=start_date, end=end_date, interval=1))

        payload = []

        for f in files:
            if 'file' in event and event['file'] not in f:
                continue

            date_range = [this_is_the_day] if not is_history or 'JUST-ONCE' in f else dates
            for date in date_range:
                payload.append(generate_script_info(f, date))

        logger.info(payload)

        return {
            "payload": payload
        }

    except Exception as e:
        logger.error(f"Error in handler function: {str(e)}")
        raise e

if __name__ == '__main__':
    handler_return = handler({
        # 'history': 'true',
        # 'start_date': '2023-08-01'
    }, None)
    print(json.dumps(handler_return, indent=4))