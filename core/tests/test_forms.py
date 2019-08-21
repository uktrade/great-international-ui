from unittest.mock import call, patch

import pytest

from core.forms import CapitalInvestContactForm


@pytest.fixture
def capital_invest_contact_form_data(captcha_stub):
    return {
        'given_name': 'Thor',
        'family_name': 'Odinson',
        'email': 'most_powerful_avenger@avengers.com',
        'phone_number': '01234 567891',
        'country': 'FR',
        'city': 'Asgard',
        'company_name': 'Guardian of the Galaxy',
        'message': 'foobar',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


def test_capital_invest_contact_form_required():
    form = CapitalInvestContactForm(
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )

    assert form.is_valid() is False
    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['country'].required is True
    assert form.fields['city'].required is False
    assert form.fields['message'].required is True
    assert form.fields['captcha'].required is True
    assert form.fields['terms_agreed'].required is True


def test_capital_invest_contact_form_accept_valid_data(captcha_stub, capital_invest_contact_form_data):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data,
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()


def test_capital_invest_contact_form_invalid_data(captcha_stub):
    form = CapitalInvestContactForm(
        data={
            'given_name': 'Steve',
            'family_name': 'Rogers',
            'country': 'FR',
            'message': 'foobar',
            'g-recaptcha-response': captcha_stub,
            'terms_agreed': True
        },
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.errors == {'email': ['This field is required.']}
    assert form.is_valid() is False


@patch.object(CapitalInvestContactForm, 'send_agent_email')
@patch.object(CapitalInvestContactForm, 'send_user_email')
def test_save_calls_send_email(
    mock_send_user_email, mock_send_agent_email,  capital_invest_contact_form_data
):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.save()

    assert mock_send_user_email.call_count == 1
    assert mock_send_agent_email.call_count == 1


@patch.object(CapitalInvestContactForm, 'action_class')
@patch.object(CapitalInvestContactForm, 'render_email', return_value='something')
def test_send_agent_email(
    mock_render_email, mock_email_action, settings, capital_invest_contact_form_data
):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.send_agent_email()

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == call(
        recipients=[settings.CAPITAL_INVEST_CONTACT_EMAIL, settings.IIGB_AGENT_EMAIL],
        subject='Capital Invest contact form lead',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
        form_url='http://www.google.com/submission_url',
        sender={
            'email_address': 'most_powerful_avenger@avengers.com',
            'country_code': 'FR'
        }
    )

    assert mock_render_email.call_count == 2
    assert mock_render_email.call_args_list[0] == call('core/capital_invest/email/capital_invest_email_agent.txt')
    assert mock_render_email.call_args_list[1] == call(
        'core/capital_invest/email/capital_invest_email_agent.html'
    )

    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == call(
        {'text_body':  'something', 'html_body': 'something'}
    )


def test_render_agent_email_context(capital_invest_contact_form_data):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )

    assert form.is_valid()

    html = form.render_email('core/capital_invest/email/capital_invest_email_agent.html')

    assert 'field_one: value_one' in html
    assert 'http://www.google.com/submission_url' in html


@patch.object(CapitalInvestContactForm, 'action_class')
@patch.object(CapitalInvestContactForm, 'render_email', return_value='something')
def test_send_user_email(
    mock_render_email, mock_email_action, settings, capital_invest_contact_form_data
):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.send_user_email()

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == call(
        recipients=[capital_invest_contact_form_data['email']],
        subject='A copy of your message and what happens next',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
        form_url='http://www.google.com/submission_url',
    )

    assert mock_render_email.call_count == 2
    assert mock_render_email.call_args_list[0] == call('core/capital_invest/email/capital_invest_email_user.txt')
    assert mock_render_email.call_args_list[1] == call('core/capital_invest/email/capital_invest_email_user.html')

    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == call(
        {'text_body':  'something', 'html_body': 'something'}
    )


@patch('core.forms.render_to_string')
def test_send_email_render_email(mock_render_to_string, capital_invest_contact_form_data):
    data = {**capital_invest_contact_form_data, 'company_website': 'http://www.google.com'}
    form = CapitalInvestContactForm(
        data=data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.render_email('hello.html')

    assert mock_render_to_string.call_count == 1
    assert mock_render_to_string.call_args == call(
        'hello.html',
        {
            'form_data': (
                ('Given name', data['given_name']),
                ('Family name', data['family_name']),
                ('Email address', data['email']),
                ('Phone number', capital_invest_contact_form_data['phone_number']),
                ('Country', data['country']),
                ('City', data['city']),
                ('Company name', data['company_name']),
                ('Message', data['message'])
            ),
            'utm': {'field_one': 'value_one'},
            'submission_url': 'http://www.google.com/submission_url'
        }
    )


@patch('core.forms.render_to_string')
def test_send_email_render_email_optional_fields(
    mock_render_to_string, capital_invest_contact_form_data
):
    form = CapitalInvestContactForm(
        data=capital_invest_contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid(), form.errors

    form.render_email('hello.html')

    assert mock_render_to_string.call_count == 1
    assert mock_render_to_string.call_args == call(
        'hello.html',
        {
            'form_data': (
                ('Given name', capital_invest_contact_form_data['given_name']),
                ('Family name', capital_invest_contact_form_data['family_name']),
                ('Email address', capital_invest_contact_form_data['email']),
                ('Phone number', capital_invest_contact_form_data['phone_number']),
                ('Country', capital_invest_contact_form_data['country']),
                ('City', capital_invest_contact_form_data['city']),
                ('Company name', capital_invest_contact_form_data['company_name']),
                ('Message', capital_invest_contact_form_data['message'])
            ),
            'utm': {'field_one': 'value_one'},
            'submission_url': 'http://www.google.com/submission_url'
        }
    )
