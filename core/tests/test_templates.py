import pytest

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


def test_article_detail_page_no_related_content(default_context):
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
        **default_context
    }

    html = render_to_string('core/article_detail.html', context)

    assert 'Related content' not in html


def test_article_detail_page_related_content(default_context):

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
                'meta': {
                    'url': '/international/test-list/test-one/',
                    'slug': 'test-one',
                    'languages': [('en-gb', 'English')],
                }
            },
            {
                'title': 'Related article 2',
                'teaser': 'Related article 2 teaser',
                'thumbnail': {'url': 'related_article_two.jpg'},
                'meta': {
                    'url': '/international/test-list/test-two/',
                    'slug': 'test-two',
                    'languages': [('en-gb', 'English')],
                }
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
        id='related-article-test-one'
    ).select('h3')[0].text == 'Related article 1'
    assert soup.find(
        id='related-article-test-two'
    ).select('h3')[0].text == 'Related article 2'


campaign_page_all_fields = {
    'campaign_heading': 'Campaign heading',
    'campaign_hero_image': {'url': 'campaign_hero_image.jpg'},
    'cta_box_button_text': 'CTA box button text',
    'cta_box_button_url': '/cta_box_button_url',
    'cta_box_message': 'CTA box message',
    'related_content_heading': 'Related content heading',
    'related_content_intro': '<p>Related content intro.</p>',
    'section_one_contact_button_text': 'Section one contact button text',
    'section_one_contact_button_url': '/section_one_contact_button_url',
    'section_one_heading': 'Section one heading',
    'section_one_image': {'url': 'section_one_image.jpg'},
    'section_one_intro': '<p>Section one intro.</p>',
    'section_two_contact_button_text': 'Section one contact button text',
    'section_two_contact_button_url': '/section_two_contact_button_url',
    'section_two_heading': 'Section two heading',
    'section_two_image': {'url': 'section_two_image.jpg'},
    'section_two_intro': '<p>Section two intro</p>',
    'selling_point_one_content': '<p>Selling point one content</p>',
    'selling_point_one_heading': 'Selling point one heading',
    'selling_point_one_icon': {'url': 'selling_point_one_icon.jpg'},
    'selling_point_two_content': '<p>Selling point two content</p>',
    'selling_point_two_heading': 'Selling point two heading',
    'selling_point_two_icon': {'url': 'selling_point_two_icon.jpg'},
    'selling_point_three_content': '<p>Selling point three content</p>',
    'selling_point_three_heading': 'Selling point three heading',
    'selling_point_three_icon': {'url': 'selling_point_three_icon.jpg'},
    'related_pages': [
        {
            'article_image': {'url': 'article_image.jpg'},
            'article_image_thumbnail': {'url': 'article1_image_thumbnail.jpg'},
            'subheading': 'Related article description 1',
            'title': 'Related article 1',
            'meta': {
                'languages': [['en-gb', 'English']],
                'url': '/international/advice/finance/article-1/',
                'slug': 'article-1'},
            'page_type': 'InternationalArticlePage',
            'title': 'Related article 1'
        },
        {
            'article_image': {'url': 'article_image.jpg'},
            'article_image_thumbnail': {'url': 'article2_image_thumbnail.jpg'},
            'subheading': 'Related article description 2',
            'title': 'Related article 2',
            'meta': {
                'languages': [['en-gb', 'English']],
                'url': '/international/advice/finance/article-2/',
                'slug': 'article-2'},
            'page_type': 'InternationalArticlePage',
            'title': 'Related article 2'
        },
        {
            'article_image': {'url': 'article_image.jpg'},
            'article_image_thumbnail': {'url': 'article3_image_thumbnail.jpg'},
            'subheading': 'Related article description 3',
            'title': 'Related article 3',
            'meta': {
                'languages': [('en-gb', 'English')],
                'url': '/international/advice/finance/article-3/',
                'slug': 'article-3'},
            'page_type': 'InternationalArticlePage',
            'title': 'Related article 3'
        },
    ],
    'meta': {
        'languages': [('en-gb', 'English')],
        'slug': 'test-page'
    },
    'page_type': 'InternationalCampaignPage'
}


def test_marketing_campaign_page_all_fields(default_context):

    context = {
        'page': campaign_page_all_fields,
        **default_context
    }

    html = render_to_string('core/campaign.html', context)

    soup = BeautifulSoup(html, 'html.parser')

    assert '<p class="body-text">Selling point two content</p>' in html

    assert '<p class="body-text">Selling point three content</p>' in html

    hero_section = soup.find(id='campaign-hero')

    exp_style = "background-image: url('{}')".format(
        campaign_page_all_fields['campaign_hero_image']['url'])

    assert hero_section.attrs['style'] == exp_style

    assert soup.find(
        id='selling-points-icon-two').attrs['src'] == campaign_page_all_fields[
        'selling_point_two_icon']['url']

    assert soup.find(
        id='selling-points-icon-three'
    ).attrs['src'] == campaign_page_all_fields[
        'selling_point_three_icon']['url']

    assert soup.find(
        id='section-one-contact-button'
    ).attrs['href'] == campaign_page_all_fields[
        'section_one_contact_button_url']
    assert soup.find(
        id='section-one-contact-button').text == campaign_page_all_fields[
        'section_one_contact_button_text']

    assert soup.find(
        id='section-two-contact-button'
    ).attrs['href'] == campaign_page_all_fields[
        'section_two_contact_button_url']
    assert soup.find(
        id='section-two-contact-button').text == campaign_page_all_fields[
        'section_two_contact_button_text']

    related_page_one = soup.find(id='related-page-article-1')
    assert related_page_one.find('a').text == 'Related article 1'
    assert related_page_one.find('p').text == 'Related article description 1'
    assert related_page_one.find('a').attrs['href'] == (
        '/international/advice/finance/article-1/')
    assert related_page_one.find('img').attrs['src'] == (
        'article1_image_thumbnail.jpg')

    related_page_two = soup.find(id='related-page-article-2')
    assert related_page_two.find('a').text == 'Related article 2'
    assert related_page_two.find('p').text == 'Related article description 2'
    assert related_page_two.find('a').attrs['href'] == (
        '/international/advice/finance/article-2/')
    assert related_page_two.find('img').attrs['src'] == (
        'article2_image_thumbnail.jpg')

    related_page_three = soup.find(id='related-page-article-3')
    assert related_page_three.find('a').text == 'Related article 3'
    assert related_page_three.find('p').text == 'Related article description 3'
    assert related_page_three.find('a').attrs['href'] == (
        '/international/advice/finance/article-3/')
    assert related_page_three.find('img').attrs['src'] == (
        'article3_image_thumbnail.jpg')


campaign_page_required_fields = {
    'campaign_heading': 'Campaign heading',
    'campaign_hero_image': None,
    'cta_box_button_text': 'CTA box button text',
    'cta_box_button_url': '/cta_box_button_url',
    'cta_box_message': 'CTA box message',
    'related_content_heading': 'Related content heading',
    'related_content_intro': '<p>Related content intro.</p>',
    'related_pages': [],
    'section_one_contact_button_text': None,
    'section_one_contact_button_url': None,
    'section_one_heading': 'Section one heading',
    'section_one_image': None,
    'section_one_intro': '<p>Section one intro.</p>',
    'section_two_contact_button_text': None,
    'section_two_contact_button_url': None,
    'section_two_heading': 'Section two heading',
    'section_two_image': None,
    'section_two_intro': '<p>Section two intro</p>',
    'selling_point_one_content': '<p>Selling point one content</p>',
    'selling_point_one_heading': 'Selling point one heading',
    'selling_point_one_icon': None,
    'selling_point_two_content': '<p>Selling point two content</p>',
    'selling_point_two_heading': 'Selling point two heading',
    'selling_point_two_icon': None,
    'selling_point_three_content': '<p>Selling point three content</p>',
    'selling_point_three_heading': 'Selling point three heading',
    'selling_point_three_icon': None,
    'meta': {
        'languages': [('en-gb', 'English')],
        'slug': 'test-page'
    },
    'page_type': 'InternationalCampaignPage'
}


def test_marketing_campaign_page_required_fields(default_context):

    context = {
        'page': campaign_page_required_fields,
        **default_context
    }

    html = render_to_string('core/campaign.html', context)

    soup = BeautifulSoup(html, 'html.parser')

    assert '<p class="body-text">Selling point two content</p>' in html
    assert '<p class="body-text">Selling point three content</p>' in html

    hero_section = soup.find(id='campaign-hero')
    assert not hero_section.attrs.get('style')

    assert not soup.find(id='selling-points-icon-two')
    assert not soup.find(id='selling-points-icon-three')

    assert not soup.find(id='section-one-contact-button')
    assert not soup.find(id='section-one-contact-button')

    assert not soup.find(id='section-two-contact-button')
    assert not soup.find(id='section-two-contact-button')

    assert soup.select(
        '#campaign-contact-box .box-heading'
        )[0].text == campaign_page_required_fields['cta_box_message']

    assert soup.find(
        id='campaign-hero-heading'
        ).text == campaign_page_required_fields['campaign_heading']

    assert soup.find(
        id='section-one-heading'
        ).text == campaign_page_required_fields['section_one_heading']

    assert soup.find(
        id='section-two-heading'
        ).text == campaign_page_required_fields['section_two_heading']

    assert soup.find(
        id='related-content-heading'
        ).text == campaign_page_required_fields['related_content_heading']

    assert soup.select(
        "li[aria-current='page']"
        )[0].text == campaign_page_required_fields['campaign_heading']


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


def test_homepage_related_pages(default_context):
    context = {
        'page': {
            'page_type': 'InternationalHomePage',
            'news_title': 'News title',
            'meta': {
                'slug': 'slug',
                'languages': [('en-gb', 'English')],
            },
            'related_pages': [
                {
                    'title': 'Related article title',
                    'page_type': 'InternationalArticlePage',
                    'teaser': 'Related article teaser',
                    'meta': {
                        'slug': 'article',
                        'languages': [('en-gb', 'English')],
                        'url': (
                            'https://great.gov.uk/international/'
                            'topic/list/article'),
                    },
                    'full_path': '/topic/list/article',
                    'full_url':
                    'https://great.gov.uk/international/topic/list/article',
                },
                {
                    'title': 'Related campaign title',
                    'page_type': 'InternationalCampaignPage',
                    'teaser': 'Related campaign teaser',
                    'meta': {
                        'slug': 'campaign',
                        'languages': [('en-gb', 'English')],
                        'url': (
                            'https://great.gov.uk/international/'
                            'campaigns/campaign'),
                    },
                    'full_path': '/international/campaigns/campaign',
                    'full_url':
                    'https://great.gov.uk/international/campaigns/campaign',
                },
            ]
        },
        **default_context
    }

    html = render_to_string('core/landing_page.html', context)

    assert 'News title' in html
    assert 'Related article title' in html
    assert 'Related article teaser' in html
    assert '/topic/list/article' in html
    assert 'Related campaign title' in html
    assert 'Related campaign teaser' in html
    assert '/international/campaigns/campaign' in html


test_localised_child_pages = [
    {
        'last_published_at': '2019-02-28T10:56:30.455848Z',
        'meta': {
            'slug': 'campaign-one',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalCampaignPage',
        'teaser': 'Campaign one teaser',
        'title': 'Campaign one'
    },
    {
        'last_published_at': '2019-02-28T10:56:31.455848Z',
        'meta': {
            'slug': 'article-one',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article one teaser',
        'title': 'Article one'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-two',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article two teaser',
        'title': 'Article two'
    },
    {
        'last_published_at': '2019-02-28T10:56:32.455848Z',
        'meta': {
            'slug': 'article-three',
            'languages': [('en-gb', 'English')],
        },
        'page_type': 'InternationalArticlePage',
        'teaser': 'Article three teaser',
        'title': 'Article three'
    },
]


@pytest.mark.parametrize('localised_articles,total_articles', (
    (
        [],
        4
    ),
    (
        test_localised_child_pages[:-3],
        5
    ),
    (
        test_localised_child_pages,
        8
    ),
))
def test_article_count_with_regional_articles(
    localised_articles, total_articles, default_context
):
    context = {
        'page': {
            'page_type': 'InternationalArticleListingPage',
            'display_title': 'Article list',
            'articles_count': 4,
            'localised_child_pages': localised_articles,
            'child_pages': [],
            'meta': {
                'slug': 'slug',
                'languages': [('en-gb', 'English')],
            },
        },
        **default_context
    }

    html = render_to_string('core/article_list.html', context)

    soup = BeautifulSoup(html, 'html.parser')
    assert '{} articles'.format(total_articles) in soup.find(
        id='hero-description').string
