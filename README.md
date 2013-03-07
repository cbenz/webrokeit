Webrokeit
=========

Minimalist events broker over HTTP written in Python.

Dependencies
------------

* MongoDB
* Python libraries: Paste, WebError, WebOb

Quick start
-----------

    mongo webrokeit --eval 'db.states.drop(); db.subscriptions.drop(); db.tasks.drop();'
    ./scripts/register_handlers.py -v ./sample_handlers/handlers.ini
    ./sample_handlers/emit_my_event_1.py -v sample_handlers/handlers.ini
    ./scripts/simple_tasks_consumer.py -v ./sample_handlers/handlers.ini

