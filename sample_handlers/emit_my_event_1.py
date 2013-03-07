#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Emit the my_event_1 event.
"""


import argparse
import ConfigParser
import json
import logging
import os
import sys
import urllib
import urllib2


log = logging.getLogger(os.path.basename(__file__))


def emit_my_event_1(handler_conf):
    event_parameters = {
        'foo': 'bar',
        }
    emit_url_data = {
        'event_name': 'my_event_1',
        'event_parameters': json.dumps(event_parameters),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    log.debug(u'Event "my_event_1" emitted with parameters: {0}.'.format(event_parameters))


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
    handler_conf = dict(config_parser.items('my_handler_1'))
    emit_my_event_1(handler_conf)
    return 0


if __name__ == '__main__':
    sys.exit(main())
