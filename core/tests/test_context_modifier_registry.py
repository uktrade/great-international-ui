import pytest
from core.context_modifiers import Registry


def test_register_non_callable():
    registry = Registry()
    with pytest.raises(TypeError):
        assert registry.register('TestPage', 'foo')


def test_register_direct():
    registry = Registry()

    def example_modifier(context, request):
        return

    registry.register('TestPage', example_modifier)

    # Confirm both methods were added to the registry
    modifiers = registry.get_for_page_type('TestPage')
    assert len(modifiers) == 1
    assert modifiers[0] == example_modifier


def test_register_as_decorator():
    registry = Registry()

    @registry.register('TestPage')
    def example_modifier(context, request):
        return

    # Confirm method was added to the registry
    modifiers = registry.get_for_page_type('TestPage')
    assert len(modifiers) == 1
    assert modifiers[0] == example_modifier


def test_register_multiple_times():
    registry = Registry()

    def example_modifier(context, request):
        return

    registry.register('TestPage', example_modifier)
    registry.register('TestPage', example_modifier)
    registry.register('TestPage', example_modifier)

    # Confirm method was only registered once
    modifiers = registry.get_for_page_type('TestPage')
    assert len(modifiers) == 1
    assert modifiers[0] == example_modifier


def test_context_modifier_register_multiple_page_types():
    registry = Registry()
    page_types = ['ArticlePage', 'EventPage', 'VenuePage']

    def example_modifier(context, request):
        return

    registry.register(page_types, example_modifier)

    # Confirm the method was added to the registry for all page types
    for page_type in page_types:
        modifiers = registry.get_for_page_type(page_type)
        assert len(modifiers) == 1
        assert modifiers[0] == example_modifier


def test_context_modifier_unregister():
    registry = Registry()
    page_types = ['ArticlePage', 'EventPage', 'VenuePage']

    def example_modifier_one(context, request):
        return

    def example_modifier_two(context, request):
        return

    registry.register(page_types, example_modifier_one)
    registry.register(page_types, example_modifier_two)

    # Check the above registry worked for both methods
    for page_type in page_types:
        modifiers = registry.get_for_page_type(page_type)
        assert len(modifiers) == 2
        assert modifiers[0] == example_modifier_one
        assert modifiers[1] == example_modifier_two

    # Now unregister one of the above modifiers
    registry.unregister(example_modifier_one)

    # Only 'example_modifier_two' should now be registered
    for page_type in page_types:
        modifiers = registry.get_for_page_type(page_type)
        assert len(modifiers) == 1
        assert modifiers[0] == example_modifier_two
