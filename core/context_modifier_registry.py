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

        if not page_type:
            return fn

        if not callable(fn):
            raise TypeError(
                'Context modifiers must be a callable, not %s' % type(fn)
            )

        if isinstance(page_type, str):
            self._add_for_page_type(page_type, fn)

        for page_type_item in page_type:
            self._add_for_page_type(page_type_item, fn)

        return fn

    def unregister(self, fn=None):
        """
        Unregisters a function as a context modifier for any page types
        that it might be registered for.

        NOTE: Use this to unregister functions used in tests to keep the
        registry nice and clean :)
        """

        if fn is None:
            def decorator(fn):
                self.unregister(fn)
                return fn
            return decorator

        for key in self.keys():
            try:
                self[key].remove(fn)
            except ValueError:
                pass

    def get_for_page_type(self, page_type):
        """
        Return a list of context modifier functions for ``page_type``.
        The list will be empty if no relevant functions have been regsitered.
        """
        return self[page_type]


context_modifier_registry = Registry()
register_context_modifier = context_modifier_registry.register
