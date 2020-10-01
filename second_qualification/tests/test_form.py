from unittest.mock import call, patch

import pytest

from second_qualification import forms


@pytest.fixture
def form_data():
    return {
        'emt_id': 42,
        'phone_number': '0000000000',
        'arrange_callback': forms.ARRANGE_CALLBACK_CHOICES[0][0],
    }


def test_second_qualification_form_required():
    form = forms.SecondQualificationForm(
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )

    assert form.is_valid() is False
    assert form.fields['phone_number'].required is True


def test_second_qualification_form_accept_valid_data(form_data):
    form = forms.SecondQualificationForm(
        data=form_data,
        utm_data={},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()


@patch.object(forms.SecondQualificationForm, 'send_agent_email')
def test_save_calls_send_email(
    mock_send_agent_email,  form_data
):
    form = forms.SecondQualificationForm(
        data=form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.save(sender_ip_address='127.0.0.1')

    assert mock_send_agent_email.call_count == 1


@patch.object(forms.SecondQualificationForm, 'action_class')
@patch.object(forms.SecondQualificationForm, 'render_email', return_value='something')
def test_send_agent_email(
    mock_render_email, mock_email_action, settings, form_data
):
    form = forms.SecondQualificationForm(
        data=form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    form.send_agent_email(sender_ip_address='127.0.0.1')

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == call(
        recipients=[settings.IIGB_AGENT_EMAIL],
        subject='Second qualification form submission',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
        form_url='http://www.google.com/submission_url',
        sender={
            'email_address': '',
            'country_code': None,
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
        {
            'text_body':  'something',
            'html_body': 'something',
            'data': {
                'phone_number': '0000000000',
                'arrange_callback': 'yes',
                'emt_id': '42',
                'telephone_contact_consent': True
            }
        }
    )


def test_render_agent_email_context(form_data):
    form = forms.SecondQualificationForm(
        data=form_data,
        utm_data={'field_one': 'value_one'},
        submission_url='http://www.google.com/submission_url'
    )
    assert form.is_valid()

    html = form.render_email('email/email_agent.html')

    assert 'field_one: value_one' in html
    assert 'http://www.google.com/submission_url' in html
