from raven.processors import SanitizePasswordsProcessor


class SanitizeEmailMessagesProcessor(SanitizePasswordsProcessor):
    KEYS = frozenset([
        'body',
    ])
