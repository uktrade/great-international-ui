from unittest.mock import patch

from django.template.loader import render_to_string

from bs4 import BeautifulSoup

dummy_page = {
    'title': 'test',
    'meta': {
        'languages': [
            ['en-gb', 'English'],
            ['fr', 'Français'],
            ['de', 'Deutsch'],
        ]
    },
    'page_type': ''
}


def test_article_detail_page_no_related_content(default_context, rf):

    test_article_page_no_related_content = {
        'title': 'Test article',
        'display_title': 'Test article',
        'subheading': 'Test teaser',
        'article_body_text': '<p>Lorem ipsum</p>',
        'related_pages': [],
        'last_published_at': '2018-10-09T16:25:13.142357Z',
        'meta': {
            'languages': [('en-gb', 'English')],
            'slug': 'foo',
        },
        'page_type': 'InternationalArticlePage',
    }

    context = {
        'page': test_article_page_no_related_content,
        'request': rf.get('/'),
        **default_context
    }

    html = render_to_string('core/article_detail.html', context)

    assert 'Related content' not in html


def test_article_detail_page_related_content(default_context, rf):

    article_page = {
        'title': 'Test article',
        'display_title': 'Test article',
        'subheading': 'Test teaser',
        'article_image': {'url': 'foobar.png'},
        'article_body_text': '<p>Lorem ipsum</p>',
        'related_pages': [
            {
                'title': 'Related article 1',
                'teaser': 'Related article 1 teaser',
                'thumbnail': {'url': 'related_article_one.jpg'},
                'full_path': '/international/test-list/test-one/',
                'meta': {
                    'slug': 'test-one',
                    'languages': [('en-gb', 'English')],
                }
            },
            {
                'title': 'Related article 2',
                'teaser': 'Related article 2 teaser',
                'thumbnail': {'url': 'related_article_two.jpg'},
                'full_path': '/international/test-list/test-two/',
                'meta': {
                    'slug': 'test-two',
                    'languages': [('en-gb', 'English')],
                },
            },
        ],
        'meta': {
            'languages': [('en-gb', 'English')],
            'slug': 'foo',
        },
        'page_type': 'InternationalArticlePage',
    }

    context = {
        'page': article_page,
        'request': rf.get('/'),
        **default_context
    }

    html = render_to_string('core/article_detail.html', context)

    assert 'Related content' in html
    soup = BeautifulSoup(html, 'html.parser')

    assert soup.find(
        id='related-article-test-one-link'
    ).attrs['href'] == '/international/test-list/test-one/'
    assert soup.find(
        id='related-article-test-two-link'
    ).attrs['href'] == '/international/test-list/test-two/'

    assert soup.find(
        id='related-article-test-one-link'
    ).text == 'Related article 1'
    assert soup.find(
        id='related-article-test-two-link'
    ).text == 'Related article 2'


def test_article_detail_page_media_rendered(default_context, rf):
    context = {
        'request': rf.get('/')
    }
    page = {
        "article_video": {
            "url": "test.mp4",
            "file_extension": "mp4"
        },
        "article_image": {
            "url": "campaign.jpg"
        }
    }

    context = {
        'page': page,
        'request': rf.get('/'),
        **default_context
    }

    html = render_to_string('core/article_detail.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    src = soup.find(id='article-video').select('source')[0]

    assert '<div class="video-container">' in html
    assert src.attrs['src'] == 'test.mp4'
    assert src.attrs['type'] == 'video/mp4'
    assert 'src="campaign.jpg"' not in html


def test_homepage_no_related_pages(default_context):
    context = {
        'page': {
            'page_type': 'InternationalHomePage',
            'news_title': 'News title',
            'meta': {
                'slug': 'slug',
                'languages': [('en-gb', 'English')],
            },
            'related_pages': []
        },
        **default_context
    }

    html = render_to_string('core/landing_page.html', context)

    assert 'News title' not in html


@patch('django.utils.translation.get_language')
def test_guide_child_articles_less_than_nine(mock_language):
    mock_language.return_value = 'fr'

    french_page = {
        'meta': {
            'languages': [['fr', 'Français']]
        }
    }
    german_page = {
        'meta': {
            'languages': [['de', 'Deutsch']]
        }
    }

    context = {
        'page': {
            'title': 'test',
            'meta': {
                'languages': [
                    ['en-gb', 'English'],
                    ['fr', 'Français'],
                    ['de', 'Deutsch'],
                ]
            },
            'page_type': '',
            'guides': [
                french_page, french_page, french_page, french_page, french_page, german_page, german_page
            ]
        }
    }

    html = render_to_string('core/uk_setup_guide/guide_landing_page.html', context)
    soup = BeautifulSoup(html, 'html.parser')

    assert len(soup.find(id='guide-articles').find_all('article')) == 5


@patch('django.utils.translation.get_language')
def test_guide_child_articles_more_than_nine(mock_language):
    mock_language.return_value = 'fr'

    french_page = {
        'meta': {
            'languages': [['fr', 'Français']]
        }
    }
    german_page = {
        'meta': {
            'languages': [['de', 'Deutsch']]
        }
    }

    context = {
        'page': {
            'title': 'test',
            'meta': {
                'languages': [
                    ['en-gb', 'English'],
                    ['fr', 'Français'],
                    ['de', 'Deutsch'],
                ]
            },
            'page_type': '',
            'guides': [
                french_page, french_page, french_page, french_page, french_page,
                french_page, french_page, french_page, french_page, french_page,
                german_page, german_page
            ]
        }
    }

    html = render_to_string('core/uk_setup_guide/guide_landing_page.html', context)
    soup = BeautifulSoup(html, 'html.parser')

    assert len(soup.find(id='guide-articles').find_all('article')) == 9
