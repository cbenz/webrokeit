#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import urllib
import urllib2


def my_handler_2(handler_conf, event_name, event_parameters):
    print u'my_handler_2: The answer to life, the universe and everything is: "{0}".'.format(
        event_parameters['answer_to_life_universe_and_everything']
        )
    return None


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'my_event_2',
        'function_name': 'my_handler_2',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None
