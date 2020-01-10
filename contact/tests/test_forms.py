from unittest.mock import call, patch

import pytest

from contact import forms


@pytest.fixture
def contact_form_data(captcha_stub):
    return {
        'name': 'Scrooge McDuck',
        'email': 'sm@example.com',
        'job_title': 'President',
        'phone_number': '0000000000',
        'company_name': 'Acme',
        'country': 'United States',
        'staff_number': forms.STAFF_CHOICES[0][0],
        'description': 'foobar',
        'email_contact_consent': False,
        'telephone_contact_consent': False,
        'g-recaptcha-response': captcha_stub,
    }


def test_contact_form_required():
    form = forms.ContactForm(
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )

    assert form.is_valid() is False
    assert form.fields['name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['job_title'].required is True
    assert form.fields['phone_number'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['company_website'].required is False
    assert form.fields['country'].required is True
    assert form.fields['staff_number'].required is True
    assert form.fields['description'].required is True
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
            'email': 'sm@example.com',
            'phone_number': '0000000000',
            'job_title': 'President',
            'company_name': 'Acme',
            'country': 'United States',
            'staff_number': forms.STAFF_CHOICES[0][0],
            'description': 'foobar',
            'email_contact_consent': False,
            'telephone_contact_consent': False,
            'g-recaptcha-response': captcha_stub
        },
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.errors == {'name': ['This field is required.']}
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
            'country_code': 'United States',
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
                ('Name', data['name']),
                ('Email address', data['email']),
                ('Job title', data['job_title']),
                ('Phone number', data['phone_number']),
                ('Company name', data['company_name']),
                ('Company website', data['company_website']),
                ('Country', data['country']),
                ('Current number of staff', data['staff_number']),
                ('Your investment', data['description']),
                ('I would like to be contacted by email', contact_form_data['email_contact_consent']),
                ('I would like to be contacted by telephone', contact_form_data['telephone_contact_consent'])
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
                ('Name', contact_form_data['name']),
                ('Email address', contact_form_data['email']),
                ('Job title', contact_form_data['job_title']),
                ('Phone number', contact_form_data['phone_number']),
                ('Company name', contact_form_data['company_name']),
                ('Company website', ''),
                ('Country', contact_form_data['country']),
                ('Current number of staff', 'Less than 10'),
                ('Your investment', contact_form_data['description']),
                ('I would like to be contacted by email', contact_form_data['email_contact_consent']),
                ('I would like to be contacted by telephone', contact_form_data['telephone_contact_consent'])
            ),
            'utm': {'field_one': 'value_one'},
            'submission_url': 'http://www.google.com/submission_url'
        }
    )
