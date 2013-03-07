#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Register handlers.
"""


import argparse
import ConfigParser
import logging
import os
import sys


log = logging.getLogger(os.path.basename(__file__))


def register_handlers(handlers_conf):
    for section_name in sorted(handlers_conf):
        handler_conf = handlers_conf[section_name]
        handler_file_path = handler_conf['handler_file']
        handler_globals = {}
        execfile(handler_file_path, handler_globals)
        register_handler_function = handler_globals['register_handler']
        handler_name = os.path.splitext(os.path.basename(handler_file_path))[0]
        log.debug(u'Calling {0}.register_handler({1})'.format(handler_name, handler_conf))
        register_handler_function(handler_conf)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('handlers_ini')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help=u'Display debug messages')
    args = parser.parse_args()
    assert os.path.isfile(args.handlers_ini)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    config_parser = ConfigParser.SafeConfigParser(defaults={
        'here': os.path.dirname(os.path.abspath(args.handlers_ini)),
        })
    config_parser.read(args.handlers_ini)
    handlers_conf = {
        section_name: dict(config_parser.items(section_name))
        for section_name in config_parser.sections()
        }
    register_handlers(handlers_conf)
    return 0


if __name__ == '__main__':
    sys.exit(main())
