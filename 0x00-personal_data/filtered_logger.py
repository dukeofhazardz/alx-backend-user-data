#!/usr/bin/env python3
""" An implementation of Personal User Data """
import re
import os
from typing import List
from logging import StreamHandler
import logging
from mysql.connector import connection

PII_FIELDS: tuple = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """ A function that returns a logging.Logger object. """
    logger = logging.getLogger("user_data")
    logger.propagate = False

    handler = StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """ A function that returns a connector to the database
        (mysql.connector.connection.MySQLConnection object) """
    username: str = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host: str = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database: str = os.getenv("PERSONAL_DATA_DB_NAME", "holberton")

    if not database:
        raise ValueError("Database env not set")

    conx = connection.MySQLConnection(user=username,
                                      password=password,
                                      host=host,
                                      database=database)
    return conx


def main() -> None:
    """ A function obtains a database connection using get_db and retrieve
    all rows in the users table and display each row under a filtered format"""
    conx = get_db()
    cursor = conx.cursor()
    cursor.execute("SELECT * FROM users")

    logger = get_logger()

    columns = [col[0] for col in cursor.description]

    for row in cursor:
        message = '; '.join((f"{c}={r}" for c, r in zip(columns, row)))
        log_record = logging.LogRecord("user_data", logging.INFO, None, None,
                                       message, None, None)
        formatted_row = logger.handlers[0].format(log_record)
        print(formatted_row)

    cursor.close()
    conx.close()


if __name__ == "__main__":
    main()
