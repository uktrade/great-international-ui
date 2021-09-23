from directory_constants import choices

from investment_atlas import forms
from investment_atlas.forms import HOW_CAN_WE_HELP_CHOICES, HOW_DID_YOU_HEAR_CHOICES


def test_high_potential_opportunity_form_serialize_data(captcha_stub):
    form = forms.ForeignDirectInvestmentOpportunityForm(
        data={
            'given_name': 'Jim',
            'family_name': 'Example',
            'job_title': 'Chief chief',
            'email_address': 'test@example.com',
            'phone_number': '555',
            'company_name': 'Example corp',
            'website_url': 'example.com',
            'company_address': '123 Some Street, \nSome town, \nSomewhere, \nNarnia',
            'country': choices.COUNTRY_CHOICES[1][0],
            'industry': [choices.INDUSTRIES[0][0]],
            'opportunities': [
                'http://www.e.com/a',
                'http://www.e.com/b',
            ],
            'how_can_we_help': HOW_CAN_WE_HELP_CHOICES[0][0],
            'your_plans': 'Lorem ipsum dolor sit amet',
            'how_did_you_hear': HOW_DID_YOU_HEAR_CHOICES[0][0],
            'email_contact_consent': True,
            'telephone_contact_consent': True,
            'g-recaptcha-response': captcha_stub,
        },
        opportunity_choices=[
            ('http://www.e.com/a', 'some great opportunity'),
            ('http://www.e.com/b', 'some other great opportunity'),
        ],
        utm_data={
            'utm_source': 'test_source',
            'utm_medium': 'test_medium',
            'utm_campaign': 'test_campaign',
            'utm_term': 'test_term',
            'utm_content': 'test_content'
        }
    )

    assert form.is_valid()
    assert form.serialized_data == {
        'given_name': 'Jim',
        'family_name': 'Example',
        'job_title': 'Chief chief',
        'email_address': 'test@example.com',
        'phone_number': '555',
        'captcha': 'PASSED',
        'company_name': 'Example corp',
        'website_url': 'example.com',
        'company_address': '123 Some Street, \nSome town, \nSomewhere, \nNarnia',
        'country': choices.COUNTRY_CHOICES[1][0],
        'industry': [choices.INDUSTRIES[0][0]],
        'opportunities': [
            'http://www.e.com/a',
            'http://www.e.com/b',
        ],
        'opportunity_urls': (
            '• some great opportunity: http://www.e.com/a\n'
            '• some other great opportunity: http://www.e.com/b'
        ),
        'how_can_we_help': HOW_CAN_WE_HELP_CHOICES[0][0],
        'your_plans': 'Lorem ipsum dolor sit amet',
        'how_did_you_hear': HOW_DID_YOU_HEAR_CHOICES[0][0],
        'email_contact_consent': True,
        'telephone_contact_consent': True,
        'utm_source': 'test_source',
        'utm_medium': 'test_medium',
        'utm_campaign': 'test_campaign',
        'utm_term': 'test_term',
        'utm_content': 'test_content'
    }


def test_hpo_form_serialize_data_without_utm_data(captcha_stub):
    form = forms.ForeignDirectInvestmentOpportunityForm(
        data={
            'given_name': 'Jim',
            'family_name': 'Example',
            'job_title': 'Chief chief',
            'email_address': 'test@example.com',
            'phone_number': '555',
            'company_name': 'Example corp',
            'website_url': 'example.com',
            'company_address': '123 Some Street, \nSome town, \nSomewhere, \nNarnia',
            'country': choices.COUNTRY_CHOICES[1][0],
            'industry': [choices.INDUSTRIES[0][0]],
            'opportunities': [
                'http://www.e.com/a',
                'http://www.e.com/b',
            ],
            'how_can_we_help': HOW_CAN_WE_HELP_CHOICES[0][0],
            'your_plans': 'Lorem ipsum dolor sit amet',
            'how_did_you_hear': HOW_DID_YOU_HEAR_CHOICES[0][0],
            'email_contact_consent': True,
            'telephone_contact_consent': True,
            'g-recaptcha-response': captcha_stub,
        },
        opportunity_choices=[
            ('http://www.e.com/a', 'some great opportunity'),
            ('http://www.e.com/b', 'some other great opportunity'),
        ],
    )

    assert form.is_valid()
    assert form.serialized_data == {
        'given_name': 'Jim',
        'family_name': 'Example',
        'job_title': 'Chief chief',
        'email_address': 'test@example.com',
        'phone_number': '555',
        'captcha': 'PASSED',
        'company_name': 'Example corp',
        'website_url': 'example.com',
        'company_address': '123 Some Street, \nSome town, \nSomewhere, \nNarnia',
        'country': choices.COUNTRY_CHOICES[1][0],
        'industry': [choices.INDUSTRIES[0][0]],
        'opportunities': [
            'http://www.e.com/a',
            'http://www.e.com/b',
        ],
        'opportunity_urls': (
            '• some great opportunity: http://www.e.com/a\n'
            '• some other great opportunity: http://www.e.com/b'
        ),
        'how_can_we_help': HOW_CAN_WE_HELP_CHOICES[0][0],
        'your_plans': 'Lorem ipsum dolor sit amet',
        'how_did_you_hear': HOW_DID_YOU_HEAR_CHOICES[0][0],
        'email_contact_consent': True,
        'telephone_contact_consent': True,
        'utm_source': '',
        'utm_medium': '',
        'utm_campaign': '',
        'utm_term': '',
        'utm_content': '',
    }
