#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Simple tasks consumer executing tasks one by one.
"""


import argparse
import ConfigParser
import logging
import os
import sys

import pymongo


log = logging.getLogger(os.path.basename(__file__))


def consume_tasks(handlers_conf, db):
    tasks_collection = db[handlers_conf['DEFAULT']['webrokeit.database.collections.tasks']]
    spec = {'status': 'PENDING'}
    while True:
        tasks_cursor = tasks_collection.find(spec).sort('created_at')
        if tasks_cursor.count() == 0:
            log.debug(u'No more pending task, quit.')
            break
        task = tasks_cursor.next()
        log.debug(u'Consuming pending task: {0}'.format(task))
        handler_globals = {}
        execfile(task['script_name'], handler_globals)
        task_function = handler_globals[task['function_name']]
        event_parameters = task.get('event_parameters') or {}
        handler_name = os.path.splitext(os.path.basename(task['script_name']))[0]
        task['status'] = 'RUNNING'
        tasks_collection.save(task, safe=True)
        try:
            task_function(handlers_conf[handler_name], task['event_name'], event_parameters)
        except StandardError, exc:
            log.exception(exc)
            task['status'] = 'ERROR'
        else:
            task['status'] = 'COMPLETE'
        tasks_collection.save(task, safe=True)
        log.debug(u'Task status is {0}'.format(task['status']))


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
    handlers_conf['DEFAULT'] = config_parser.defaults()
    connection = pymongo.Connection(
        host=handlers_conf['DEFAULT']['webrokeit.database.host_name'],
        port=int(handlers_conf['DEFAULT']['webrokeit.database.port']),
        )
    db = connection[handlers_conf['DEFAULT']['webrokeit.database.name']]
    consume_tasks(handlers_conf, db)
    return 0


if __name__ == '__main__':
    sys.exit(main())
