# -*- coding: utf-8 -*-


"""Paste INI configuration"""


import logging
import os

from biryani1 import strings
from biryani1.baseconv import check, default, function, guess_bool, input_to_int, pipe, struct


def load_configuration(global_conf, app_conf):
    """Build the application configuration dict."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {}
    conf.update(strings.deep_decode(global_conf))
    conf.update(strings.deep_decode(app_conf))
    conf.update(check(struct(
        {
            'app_conf': default(app_conf),
            'app_dir': default(app_dir),
            'cache_dir': default(os.path.join(os.path.dirname(app_dir), 'cache')),
            'database.collections.states': default('states'),
            'database.collections.subscriptions': default('subscriptions'),
            'database.collections.tasks': default('tasks'),
            'database.host_name': default('localhost'),
            'database.name': default('webrokeit'),
            'database.port': pipe(input_to_int, default(27017)),
            'debug': pipe(guess_bool, default(False)),
            'global_conf': default(global_conf),
            'log_level': pipe(
                default('WARNING'),
                function(lambda log_level: getattr(logging, log_level.upper())),
                ),
            'package_name': default('webrokeit'),
        },
        default='drop',
        drop_none_values=False,
    ))(conf))
    return conf
