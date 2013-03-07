#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import urllib
import urllib2


def my_handler_1(handler_conf, event_name, event_parameters):
    print 'my_handler_1: doing something.'
    emit_url_data = {
        'event_name': 'my_event_2',
        'event_parameters': json.dumps({
            'answer_to_life_universe_and_everything': 42,
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'my_event_1',
        'function_name': 'my_handler_1',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None
