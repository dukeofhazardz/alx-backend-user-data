#!/usr/bin/env python3
""" An implementation of Personal User Data """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ A function that returns the log message obfuscated """
    pattern = rf'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, f'\\1={redaction}', message)
