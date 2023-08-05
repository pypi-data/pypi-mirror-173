"""MR Git - multi-repositories git utility.
-----

See https://github.com/pbauermeister/mr-git for information, syntax and
examples.

-----

This module does pretty much all the work for now.

"""

import argparse
import os
import re
import sys


def parse_args() -> argparse.Namespace:
    description, epilog = [each.strip() for each in __doc__.split('-----')[:2]]

    parser = argparse.ArgumentParser(description=description, epilog=epilog)

    parser.add_argument('--debug',
                        action='store_true',
                        default=False,
                        help='emits debug messages')
    return parser.parse_args()


def main() -> None:
    """Entry point for the application script"""
    args = parse_args()

    print("Hello world.")
