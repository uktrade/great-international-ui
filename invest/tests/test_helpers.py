import pytest

from invest import helpers


@pytest.mark.parametrize('path,expected_prefix', (
    ('/es/industries/', 'es'),
    ('/zh-hans/industries/', 'zh-hans'),
    ('/de/industries/aerospace/', 'de'),
    ('/fr/industries/free-foods/', 'fr'),
))
def test_get_language_from_prefix(path, expected_prefix):
    prefix = helpers.get_language_from_prefix(path)
    assert prefix == expected_prefix
