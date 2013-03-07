Webrokeit
=========

Minimalist events broker over HTTP written in Python.

Quick start
-----------

    ./scripts/register_handlers.py -v ./sample_handlers/handlers.ini
    ./sample_handlers/emit_my_event_1.py -v sample_handlers/handlers.ini
    ./scripts/simple_tasks_consumer.py -v ./sample_handlers/handlers.ini

Reset database
--------------

    mongo webrokeit --eval 'db.states.drop(); db.subscriptions.drop(); db.tasks.drop();'
