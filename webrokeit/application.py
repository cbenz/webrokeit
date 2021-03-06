# -*- coding: utf-8 -*-


"""Middleware initialization"""


import logging
import sys

from weberror.errormiddleware import ErrorMiddleware

from . import configuration, context, controllers, database, templates


def make_app(global_conf, **app_conf):
    app_ctx = context.Context()
    app_ctx.conf = configuration.load_configuration(global_conf, app_conf)
    logging.basicConfig(level=app_ctx.conf['log_level'], stream=sys.stdout)
    app_ctx.db = database.load_database(app_ctx)
    app_ctx.templates = templates.load_templates(app_ctx)
    database.ensure_indexes(app_ctx)
    app = controllers.make_router()
    app = context.make_add_context_to_request(app, app_ctx)
    if not app_ctx.conf['debug']:
        app = ErrorMiddleware(
            app,
            error_email=app_ctx.conf['email_to'],
            error_log=app_ctx.conf.get('error_log', None),
            error_message=app_ctx.conf.get('error_message', u'An internal server error occurred'),
            error_subject_prefix=app_ctx.conf.get('error_subject_prefix', u'Web application error: '),
            from_address=app_ctx.conf['from_address'],
            smtp_server=app_ctx.conf.get('smtp_server', 'localhost'),
        )
    app.ctx = app_ctx
    return app
