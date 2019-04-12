from django.template.loader import render_to_string

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


def test_homepage_button_how_to_do_business_feature_off():

    page = dummy_page
    page['hero_cta_text'] = 'Hero CTA text'

    context = {
        'page': page,
        'features': {
            'HOW_TO_DO_BUSINESS_ON': False,
        }
    }

    template_name = 'core/landing_page.html'
    html = render_to_string(template_name, context)

    assert 'Hero CTA text' not in html


def test_homepage_button_how_to_do_business_feature_on():

    page = dummy_page
    page['hero_cta_text'] = 'Hero CTA text'

    context = {
        'page': page,
        'features': {
            'HOW_TO_DO_BUSINESS_ON': True,
        }
    }

    template_name = 'core/landing_page.html'
    html = render_to_string(template_name, context)

    assert 'Hero CTA text' in html
