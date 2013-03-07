# -*- coding: utf-8 -*-


import datetime

from biryani1.baseconv import check
from webob.dec import wsgify

from . import conv, router, wsgi_helpers


@wsgify
def emit(req):
    assert req.method == 'POST'
    data, errors = conv.params_to_emit_data(req.params)
    if errors is not None:
        return wsgi_helpers.respond_json(req.ctx, {'errors': errors}, code=400)
    spec = {'event_name': data['event_name']}
    subscriptions_collection = req.ctx.db[req.ctx.conf['database.collections.subscriptions']]
    tasks_collection = req.ctx.db[req.ctx.conf['database.collections.tasks']]
    subscribers_cursor = subscriptions_collection.find(spec)
    for subscriber in subscribers_cursor:
        task = {
            'created_at': datetime.datetime.now(),
            'event_name': data['event_name'],
            'event_parameters': data['event_parameters'],
            'function_name': subscriber['function_name'],
            'script_name': subscriber['script_name'],
            'status': 'PENDING',
            }
        tasks_collection.save(task)
    return wsgi_helpers.respond_json(req.ctx, None)


def make_router():
    """Return a WSGI application that dispatches requests to controllers """
    return router.make_router(
        ('POST', '^/emit$', emit),
        ('POST', '^/state$', state),
        ('POST', '^/subscribe$', subscribe),
        )


@wsgify
def state(req):
    assert req.method == 'POST'
    data, errors = conv.params_to_state_data(req.params)
    if errors is not None:
        return wsgi_helpers.respond_json(req.ctx, {'errors': errors}, code=400)
    states_collection = req.ctx.db[req.ctx.conf['database.collections.states']]
    if data['action'] == 'save':
        state_document = {
            'created_at': datetime.datetime.now(),
            'data': data['data'],
            'key': data['key'],
            }
        states_collection.save(state_document)
    spec = {'key': data['key']}
    state_document_list = [
        check(conv.state_document_to_json(state_document))
        for state_document in states_collection.find(spec).sort('created_at')
        ]
    return wsgi_helpers.respond_json(req.ctx, state_document_list)


@wsgify
def subscribe(req):
    assert req.method == 'POST'
    data, errors = conv.params_to_subscribe_data(req.params)
    if errors is not None:
        return wsgi_helpers.respond_json(req.ctx, {'errors': errors}, code=400)
    # TODO Subscribe only if not already subscribed.
    subscriptions_collection = req.ctx.db[req.ctx.conf['database.collections.subscriptions']]
    data['created_at'] = datetime.datetime.now()
    subscriptions_collection.save(data)
    return wsgi_helpers.respond_json(req.ctx, None)
