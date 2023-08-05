#!/usr/bin/env python

import sys

import argparse
import logging
import pydash as _

from .log import clilog
from .conn import conn_main


def main():
    clilog('EC5 CONN', color='blue', figlet=True)
    clilog('Welcome to EC5 CONN\n', 'green')

    ap = argparse.ArgumentParser(description='ec5 conn')
    ap.add_argument('--mode', '-m', type=str, dest='mode',
                    default='conn', help='ec5 conn mode')
    ap.add_argument('--debug', '-d', dest='debug', default=False,
                    action='store_true', help='Debug-mode')
    args, _unknown = ap.parse_known_args()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(format='%(message)s', level=log_level)
    logger = logging.getLogger(__name__)

    mode = _.get(args, 'mode')
    logger.debug(f'mode = {mode}')

    if mode == 'conn':
        return conn_main()

    clilog(f'Not impemented mode, mode={mode}', 'red')
    return 1


if __name__ == '__main__':
    sys.exit(main())
