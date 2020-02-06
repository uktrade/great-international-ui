from unittest.mock import call, patch

import pytest

from contact import forms


@pytest.fixture
def contact_form_data(captcha_stub):
    return {
        'given_name': 'Scrooge',
        'family_name': 'McDuck',
        'job_title': 'President',
        'email': 'sm@example.com',
        'phone_number': '0000000000',
        'company_name': 'Acme',
        'company_website': 'www.test.com',
        'company_hq_address': 'London',
        'country': forms.COUNTRY_CHOICES[0][0],
        'industry': forms.INDUSTRIES[0][0],
        'expanding_to_uk': forms.EXPANDING_TO_UK_CHOICES[1][0],
        'description': 'lorum ipsum',
        'arrange_callback': forms.ARRANGE_CALLBACK_CHOICES[0][0],
        'when_to_call': 'in the morning',
        'how_did_you_hear': forms.HOW_DID_YOU_HEAR_CHOICES[1][0],
        'email_contact_consent': False,
        'telephone_contact_consent': False,
        'g-recaptcha-response': captcha_stub
    }


def test_contact_form_required():
    form = forms.ContactForm(
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )

    assert form.is_valid() is False
    assert form.fields['given_name'].required is True
    assert form.fields['family_name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['job_title'].required is True
    assert form.fields['phone_number'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['company_hq_address'].required is True
    assert form.fields['country'].required is True
    assert form.fields['industry'].required is True
    assert form.fields['expanding_to_uk'].required is True
    assert form.fields['description'].required is False
    assert form.fields['arrange_callback'].required is True
    assert form.fields['arrange_callback'].nested_form.fields['when_to_call'].required is False
    assert form.fields['captcha'].required is True


def test_contact_form_accept_valid_data(captcha_stub, contact_form_data):
    form = forms.ContactForm(
        data=contact_form_data,
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()


def test_contact_form_invalid_data(captcha_stub):
    form = forms.ContactForm(
        data={
            'company_website': 'www.google.com',
            'company_hq_address': 'London',
            'email': 'sm@example.com',
            'phone_number': '0000000000',
            'job_title': 'President',
            'company_name': 'Acme',
            'how_did_you_hear': forms.HOW_DID_YOU_HEAR_CHOICES[1][0],
            'email_contact_consent': False,
            'telephone_contact_consent': False,
            'g-recaptcha-response': captcha_stub
        },
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )

    assert form.errors == {
        'given_name': ['This field is required.'],
        'family_name': ['This field is required.'],
        'country': ['This field is required.'],
        'industry': ['This field is required.'],
        'expanding_to_uk': ['This field is required.'],
        'arrange_callback': ['This field is required.']
    }
    assert form.is_valid() is False


@patch.object(forms.ContactForm, 'send_agent_email')
@patch.object(forms.ContactForm, 'send_user_email')
def test_save_calls_send_email(
    mock_send_user_email, mock_send_agent_email,  contact_form_data
):
    form = forms.ContactForm(
        data=contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.save(sender_ip_address='127.0.0.1')

    assert mock_send_user_email.call_count == 1
    assert mock_send_agent_email.call_count == 1


@patch.object(forms.ContactForm, 'action_class')
@patch.object(forms.ContactForm, 'render_email', return_value='something')
def test_send_agent_email(
    mock_render_email, mock_email_action, settings, contact_form_data
):
    form = forms.ContactForm(
        data=contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.send_agent_email(sender_ip_address='127.0.0.1')

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == call(
        recipients=[settings.IIGB_AGENT_EMAIL],
        subject='Contact form agent email subject',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
        form_url='http://www.google.com/submission_url',
        sender={
            'email_address': 'sm@example.com',
            'country_code': forms.COUNTRY_CHOICES[0][0],
            'ip_address': '127.0.0.1',
        }
    )

    assert mock_render_email.call_count == 2
    assert mock_render_email.call_args_list[0] == call('email/email_agent.txt')
    assert mock_render_email.call_args_list[1] == call(
        'email/email_agent.html'
    )

    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == call(
        {'text_body':  'something', 'html_body': 'something'}
    )


def test_render_agent_email_context(contact_form_data):
    form = forms.ContactForm(
        data=contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    html = form.render_email('email/email_agent.html')

    assert 'field_one: value_one' in html
    assert 'http://www.google.com/submission_url' in html


@patch.object(forms.ContactForm, 'action_class')
@patch.object(forms.ContactForm, 'render_email', return_value='something')
def test_send_user_email(
    mock_render_email, mock_email_action, settings, contact_form_data
):
    form = forms.ContactForm(
        data=contact_form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.send_user_email()

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == call(
        recipients=[contact_form_data['email']],
        subject='Contact form user email subject',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
        form_url='http://www.google.com/submission_url',
    )

    assert mock_render_email.call_count == 2
    assert mock_render_email.call_args_list[0] == call('email/email_user.txt')
    assert mock_render_email.call_args_list[1] == call('email/email_user.html')

    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == call(
        {'text_body':  'something', 'html_body': 'something'}
    )


@patch('contact.forms.render_to_string')
def test_send_email_render_email(mock_render_to_string, contact_form_data):
    data = {**contact_form_data, 'company_website': 'http://www.google.com'}
    form = forms.ContactForm(
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
                ('Job title', data['job_title']),
                ('Email address', data['email']),
                ('Phone number', data['phone_number']),
                ('Company name', data['company_name']),
                ('Company website', data['company_website']),
                ('Company HQ address', data['company_hq_address']),
                ('Country', data['country']),
                ('Industry', data['industry']),
                ('Which of these best describes how you feel about expanding to the UK?', data['expanding_to_uk']),
                ('Tell us about your investment', data['description']),
                ('Would you like us to arrange a call?', data['arrange_callback']),
                ('When should we call you?', data['when_to_call']),
                ('How did you hear about us?', data['how_did_you_hear']),
                ('I would like to receive additional information by email', contact_form_data['email_contact_consent']),
                (
                    'I would like to receive additional information by telephone',
                    contact_form_data['telephone_contact_consent']
                )
            ),
            'utm': {'field_one': 'value_one'},
            'submission_url': 'http://www.google.com/submission_url'
        }
    )


@patch('contact.forms.render_to_string')
def test_send_email_render_email_optional_fields(
    mock_render_to_string, contact_form_data
):
    form = forms.ContactForm(
        data=contact_form_data,
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
                ('Given name', contact_form_data['given_name']),
                ('Family name', contact_form_data['family_name']),
                ('Job title', contact_form_data['job_title']),
                ('Email address', contact_form_data['email']),
                ('Phone number', contact_form_data['phone_number']),
                ('Company name', contact_form_data['company_name']),
                ('Company website', contact_form_data['company_website']),
                ('Company HQ address', contact_form_data['company_hq_address']),
                ('Country', contact_form_data['country']),
                ('Industry', contact_form_data['industry']),
                ('Which of these best describes how you feel about expanding to the UK?',
                    contact_form_data['expanding_to_uk']),
                ('Tell us about your investment', contact_form_data['description']),
                ('Would you like us to arrange a call?', contact_form_data['arrange_callback']),
                ('When should we call you?', contact_form_data['when_to_call']),
                ('How did you hear about us?', contact_form_data['how_did_you_hear']),
                ('I would like to receive additional information by email', contact_form_data['email_contact_consent']),
                (
                    'I would like to receive additional information by telephone',
                    contact_form_data['telephone_contact_consent']
                )
            ),
            'utm': {'field_one': 'value_one'},
            'submission_url': 'http://www.google.com/submission_url'
        }
    )
