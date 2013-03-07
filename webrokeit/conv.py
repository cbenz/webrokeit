# -*- coding: utf-8 -*-


from biryani1.baseconv import cleanup_line, noop, not_none, pipe, set_value, struct, test_in
from biryani1.datetimeconv import datetime_to_iso8601_str
from biryani1.jsonconv import make_input_to_json


input_to_json = make_input_to_json()


params_to_emit_data = struct(
    {
        'event_name': pipe(cleanup_line, not_none),
        'event_parameters': input_to_json,
        },
    drop_none_values=False,
    )


params_to_state_data = struct(
    {
        'action': pipe(cleanup_line, test_in(['find', 'save'])),
        'data': pipe(input_to_json, not_none),
        'key': pipe(cleanup_line, not_none),
        },
    drop_none_values=False,
    )


params_to_subscribe_data = struct(
    {
        'event_name': pipe(cleanup_line, not_none),
        'function_name': pipe(cleanup_line, not_none),
        'script_name': pipe(cleanup_line, not_none),
        },
    drop_none_values=False,
    )


state_document_to_json = pipe(
    struct(
        {
            '_id': set_value(None),
            'created_at': datetime_to_iso8601_str,
            },
        default=noop,
        drop_none_values=True,
        ),
    )
