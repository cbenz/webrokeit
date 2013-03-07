# -*- coding: utf-8 -*-


"""Database loading function."""


import pymongo


def ensure_indexes(ctx):
    subscriptions_collection = ctx.db[ctx.conf['database.collections.subscriptions']]
    tasks_collection = ctx.db[ctx.conf['database.collections.tasks']]
    subscriptions_collection.ensure_index([('event_name', pymongo.ASCENDING)])
    tasks_collection.ensure_index([('status', pymongo.ASCENDING)])
    return None


def load_database(ctx):
    connection = pymongo.Connection(host=ctx.conf['database.host_name'], port=ctx.conf['database.port'])
    db = connection[ctx.conf['database.name']]
    return db
