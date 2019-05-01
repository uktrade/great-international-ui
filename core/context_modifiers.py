from collections import defaultdict


class Registry(defaultdict):

    def __init__(self):
        super().__init__(list)

    def register(self, context_modifier, *for_page_types):
        """
        Registers a function or class as a context modifier
        for pages of type `page_type`
        """

        if not for_page_types:
            return context_modifier

        if not callable(context_modifier):
            raise TypeError('Context modifiers must be callables')

        for page_type in for_page_types:
            if context_modifier not in self[page_type]:
                self[page_type].append(context_modifier)

        return context_modifier

    def register_decorator(self, context_modifier=None, *for_page_types):
        """
        Register a model as a setting in the Wagtail admin
        """
        if context_modifier is None:
            return lambda context_modifier: self.register(
                context_modifier, *for_page_types)
        return self.register(context_modifier, *for_page_types)

    def get_for_page_type(self, page_type):
        return self[page_type]


registry = Registry()
register_context_modifier = registry.register_decorator
