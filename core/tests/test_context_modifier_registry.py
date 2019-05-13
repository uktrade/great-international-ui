import pytest
from core.context_modifiers import Registry

context_modifiers = Registry()


def test_context_modifier_register():

    @context_modifiers.register('TestPage')
    def test_page_context_modifier(context, request):
        return {}

    modifiers = context_modifiers.get_for_page_type('TestPage')
    assert len(modifiers) == 1
    assert modifiers[0] == test_page_context_modifier


def test_context_modifier_not_callable():
    with pytest.raises(TypeError):
        assert context_modifiers.register('TestPage', 'foo')
