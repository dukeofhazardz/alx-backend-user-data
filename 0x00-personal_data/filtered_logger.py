#!/usr/bin/env python3
""" An implementation of Personal User Data """

import re


def filter_datum(fields: list, redaction: str, message: str, separator: str):
    """ A function that returns the log message obfuscated """
    pattern = rf'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, f'\\1={redaction}', message)
