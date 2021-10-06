from investment_atlas import helpers


def test_get_sectors_label():
    page = {  # NOQA
        'related_sectors': [
            {'related_sector': {'title': 'Housing'}},
            {'related_sector': {'title': 'Aerospace'}}
        ],
        'sub_sectors': ['Green housing', 'Urban', 'Renting']
    }

    assert helpers.get_sectors_label(page) == 'Housing (Green housing, Urban, Renting)'


def test_get_sectors_label_undefined_sectors():
    page = {}

    assert helpers.get_sectors_label(page) == ''


def test_get_sectors_label_undefined_sub_sectors():
    page = {  # NOQA
        'related_sectors': [
            {'related_sector': {'title': 'Housing'}}
        ]
    }

    assert helpers.get_sectors_label(page) == 'Housing'


def test_get_sectors_label_no_sector():
    page = {  # NOQA
        'related_sectors': [],
        'sub_sectors': ['Green housing', 'Urban', 'Renting']
    }

    assert helpers.get_sectors_label(page) == ''


def test_get_sectors_label_no_subsectors():
    page = {  # NOQA
        'related_sectors': [
            {'related_sector': {'title': 'Housing'}},
            {'related_sector': {'title': 'Aerospace'}}
        ],
        'sub_sectors': []
    }

    assert helpers.get_sectors_label(page) == 'Housing'


def test_get_sectors_label_blank_sector():
    page = {  # NOQA
        'related_sectors': [
            {'related_sector': []}
        ]
    }

    assert helpers.get_sectors_label(page) == ''


def test_get_sectors_label_blank_sub_sector():
    page = {  # NOQA
        'related_sectors': [
            {'related_sector': {'title': 'Housing'}},
        ],
        'sub_sectors': ['']
    }

    assert helpers.get_sectors_label(page) == 'Housing'
