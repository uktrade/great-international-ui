import pytest

from invest.templatetags.invest_tags import get_first_heading


@pytest.mark.parametrize('html, expected', [
    ('<h1>Heading</h1><p>A paragraph.</p><h2>Another heading</h2>', 'Heading'),
    ('<p>A paragraph.</p><h2>Another heading</h2>', 'Another heading'),
    ('<h3>Heading</h3><p>A paragraph.</p>', 'Heading')
])
def test_get_heading(html, expected):
    assert get_first_heading(html) == expected
