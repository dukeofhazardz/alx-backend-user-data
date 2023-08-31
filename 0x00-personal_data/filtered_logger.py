#!/usr/bin/env python3
""" An implementation of Personal User Data """
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initializes the RedactingFormatter Class """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter values in incoming log records using filter_datum. """
        log_message = filter_datum(self.fields, self.REDACTION,
                                   super().format(record), self.SEPARATOR)
        return log_message


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ A function that returns the log message obfuscated """
    pattern = rf'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, f'\\1={redaction}', message)
