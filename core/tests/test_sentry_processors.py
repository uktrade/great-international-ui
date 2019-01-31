from unittest.mock import Mock

import raven

from core import sentry_processors


def get_stack_trace_data_real(data):
    # https://github.com/getsentry/raven-python/blob/
    # master/tests/processors/tests.py#L27
    def throw_type_error(data):
        raise TypeError()
    client = raven.Client('http://public:secret@sentry.local/1')
    try:
        throw_type_error(data)
    except TypeError:
        return client.build_msg('raven.events.Exception')


def test_email_sanitize_subject_body():
    input_data = {
        'body': 'hi',
        'thing': 'things',
    }
    data = get_stack_trace_data_real(input_data)
    proc = sentry_processors.SanitizeEmailMessagesProcessor(Mock())
    result = proc.process(data)

    vars = result['exception']['values'][-1]['stacktrace']['frames'][1]['vars']

    assert vars['data']["'body'"] == '********'
