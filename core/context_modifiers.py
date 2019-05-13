from collections import defaultdict


class Registry(defaultdict):

    def __init__(self):
        super().__init__(list)

    def _add_for_page_type(self, page_type, fn):
        if fn not in self[page_type]:
            self[page_type].append(fn)

    def register(self, page_type, fn=None):
        """
        Registers a function as a context modifier for pages of type
        ``page_type`` (which may be a single string, or a list).
        """

        if fn is None:
            def decorator(fn):
                self.register(page_type, fn)
                return fn
            return decorator

        if not callable(fn):
            raise TypeError(
                'Context modifiers must be a callables, not %s' % type(fn)
            )

        if isinstance(page_type, str):
            self._add_for_page_type(page_type, fn)

        for page_type_item in page_type:
            self._add_for_page_type(page_type_item, fn)

        return fn

    def get_for_page_type(self, page_type):
        return self[page_type]
