from captcha.fields import ReCaptchaField
from directory_components import forms, fields
from directory_forms_api_client.actions import EmailAction

from django.conf import settings
from django.forms import Textarea, Select
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


COUNTRIES = (
    ("Afghanistan", "Afghanistan"),
    ("Albania", "Albania"),
    ("Algeria", "Algeria"),
    ("American Samoa", "American Samoa"),
    ("Andorra", "Andorra"),
    ("Angola", "Angola"),
    ("Anguilla", "Anguilla"),
    ("Antigua and Barbuda", "Antigua and Barbuda"),
    ("Argentina", "Argentina"),
    ("Armenia", "Armenia"),
    ("Aruba", "Aruba"),
    ("Australia", "Australia"),
    ("Austria", "Austria"),
    ("Azerbaijan", "Azerbaijan"),
    ("The Bahamas", "The Bahamas"),
    ("Bahrain", "Bahrain"),
    ("Bangladesh", "Bangladesh"),
    ("Barbados", "Barbados"),
    ("Belarus", "Belarus"),
    ("Belgium", "Belgium"),
    ("Belize", "Belize"),
    ("Benin", "Benin"),
    ("Bermuda", "Bermuda"),
    ("Bhutan", "Bhutan"),
    ("Bolivia", "Bolivia"),
    ("Bosnia and Herzegovina", "Bosnia and Herzegovina"),
    ("Botswana", "Botswana"),
    ("Brazil", "Brazil"),
    ("Brunei", "Brunei"),
    ("Bulgaria", "Bulgaria"),
    ("Burkina Faso", "Burkina Faso"),
    ("Burundi", "Burundi"),
    ("Cambodia", "Cambodia"),
    ("Cameroon", "Cameroon"),
    ("Canada", "Canada"),
    ("Cape Verde", "Cape Verde"),
    ("Cayman Islands", "Cayman Islands"),
    ("Central African Republic", "Central African Republic"),
    ("Chad", "Chad"),
    ("Chile", "Chile"),
    ("People 's Republic of China", "People 's Republic of China"),
    ("Republic of China", "Republic of China"),
    ("Christmas Island", "Christmas Island"),
    ("Cocos(Keeling) Islands", "Cocos(Keeling) Islands"),
    ("Colombia", "Colombia"),
    ("Comoros", "Comoros"),
    ("Congo", "Congo"),
    ("Cook Islands", "Cook Islands"),
    ("Costa Rica", "Costa Rica"),
    ("Cote d'Ivoire", "Cote d'Ivoire"),
    ("Croatia", "Croatia"),
    ("Cuba", "Cuba"),
    ("Cyprus", "Cyprus"),
    ("Czech Republic", "Czech Republic"),
    ("Denmark", "Denmark"),
    ("Djibouti", "Djibouti"),
    ("Dominica", "Dominica"),
    ("Dominican Republic", "Dominican Republic"),
    ("Ecuador", "Ecuador"),
    ("Egypt", "Egypt"),
    ("El Salvador", "El Salvador"),
    ("Equatorial Guinea", "Equatorial Guinea"),
    ("Eritrea", "Eritrea"),
    ("Estonia", "Estonia"),
    ("Ethiopia", "Ethiopia"),
    ("Falkland Islands", "Falkland Islands"),
    ("Faroe Islands", "Faroe Islands"),
    ("Fiji", "Fiji"),
    ("Finland", "Finland"),
    ("France", "France"),
    ("French Polynesia", "French Polynesia"),
    ("Gabon", "Gabon"),
    ("The Gambia", "The Gambia"),
    ("Georgia", "Georgia"),
    ("Germany", "Germany"),
    ("Ghana", "Ghana"),
    ("Gibraltar", "Gibraltar"),
    ("Greece", "Greece"),
    ("Greenland", "Greenland"),
    ("Grenada", "Grenada"),
    ("Guadeloupe", "Guadeloupe"),
    ("Guam", "Guam"),
    ("Guatemala", "Guatemala"),
    ("Guernsey", "Guernsey"),
    ("Guinea", "Guinea"),
    ("Guinea - Bissau", "Guinea - Bissau"),
    ("Guyana", "Guyana"),
    ("Haiti", "Haiti"),
    ("Honduras", "Honduras"),
    ("Hong Kong", "Hong Kong"),
    ("Hungary", "Hungary"),
    ("Iceland", "Iceland"),
    ("India", "India"),
    ("Indonesia", "Indonesia"),
    ("Iran", "Iran"),
    ("Iraq", "Iraq"),
    ("Ireland", "Ireland"),
    ("Israel", "Israel"),
    ("Italy", "Italy"),
    ("Jamaica", "Jamaica"),
    ("Japan", "Japan"),
    ("Jersey", "Jersey"),
    ("Jordan", "Jordan"),
    ("Kazakhstan", "Kazakhstan"),
    ("Kenya", "Kenya"),
    ("Kiribati", "Kiribati"),
    ("North Korea", "North Korea"),
    ("South Korea", "South Korea"),
    ("Kosovo", "Kosovo"),
    ("Kuwait", "Kuwait"),
    ("Kyrgyzstan", "Kyrgyzstan"),
    ("Laos", "Laos"),
    ("Latvia", "Latvia"),
    ("Lebanon", "Lebanon"),
    ("Lesotho", "Lesotho"),
    ("Liberia", "Liberia"),
    ("Libya", "Libya"),
    ("Liechtenstein", "Liechtenstein"),
    ("Lithuania", "Lithuania"),
    ("Luxembourg", "Luxembourg"),
    ("Macau", "Macau"),
    ("Macedonia", "Macedonia"),
    ("Madagascar", "Madagascar"),
    ("Malawi", "Malawi"),
    ("Malaysia", "Malaysia"),
    ("Maldives", "Maldives"),
    ("Mali", "Mali"),
    ("Malta", "Malta"),
    ("Marshall Islands", "Marshall Islands"),
    ("Martinique", "Martinique"),
    ("Mauritania", "Mauritania"),
    ("Mauritius", "Mauritius"),
    ("Mayotte", "Mayotte"),
    ("Mexico", "Mexico"),
    ("Micronesia", "Micronesia"),
    ("Moldova", "Moldova"),
    ("Monaco", "Monaco"),
    ("Mongolia", "Mongolia"),
    ("Montenegro", "Montenegro"),
    ("Montserrat", "Montserrat"),
    ("Morocco", "Morocco"),
    ("Mozambique", "Mozambique"),
    ("Myanmar", "Myanmar"),
    ("Nagorno - Karabakh", "Nagorno - Karabakh"),
    ("Namibia", "Namibia"),
    ("Nauru", "Nauru"),
    ("Nepal", "Nepal"),
    ("Netherlands", "Netherlands"),
    ("Netherlands Antilles", "Netherlands Antilles"),
    ("New Caledonia", "New Caledonia"),
    ("New Zealand", "New Zealand"),
    ("Nicaragua", "Nicaragua"),
    ("Niger", "Niger"),
    ("Nigeria", "Nigeria"),
    ("Niue", "Niue"),
    ("Norfolk Island", "Norfolk Island"),
    ("Turkish Republic of Northern Cyprus", "Turkish Republic of Northern Cyprus"),  # noqa: E501
    ("Northern Mariana", "Northern Mariana"),
    ("Norway", "Norway"),
    ("Oman", "Oman"),
    ("Pakistan", "Pakistan"),
    ("Palau", "Palau"),
    ("Palestine", "Palestine"),
    ("Panama", "Panama"),
    ("Papua New Guinea", "Papua New Guinea"),
    ("Paraguay", "Paraguay"),
    ("Peru", "Peru"),
    ("Philippines", "Philippines"),
    ("Pitcairn Islands", "Pitcairn Islands"),
    ("Poland", "Poland"),
    ("Portugal", "Portugal"),
    ("Puerto Rico", "Puerto Rico"),
    ("Qatar", "Qatar"),
    ("Romania", "Romania"),
    ("Russia", "Russia"),
    ("Rwanda", "Rwanda"),
    ("Saint Barthelemy", "Saint Barthelemy"),
    ("Saint Helena", "Saint Helena"),
    ("Saint Kitts and Nevis", "Saint Kitts and Nevis"),
    ("Saint Lucia", "Saint Lucia"),
    ("Saint Martin", "Saint Martin"),
    ("Saint Pierre and Miquelon", "Saint Pierre and Miquelon"),
    ("Saint Vincent and the Grenadines", "Saint Vincent and the Grenadines"),
    ("Samoa", "Samoa"),
    ("San Marino", "San Marino"),
    ("Sao Tome and Principe", "Sao Tome and Principe"),
    ("Saudi Arabia", "Saudi Arabia"),
    ("Senegal", "Senegal"),
    ("Serbia", "Serbia"),
    ("Seychelles", "Seychelles"),
    ("Sierra Leone", "Sierra Leone"),
    ("Singapore", "Singapore"),
    ("Slovakia", "Slovakia"),
    ("Slovenia", "Slovenia"),
    ("Solomon Islands", "Solomon Islands"),
    ("Somalia", "Somalia"),
    ("Somaliland", "Somaliland"),
    ("South Africa", "South Africa"),
    ("South Ossetia", "South Ossetia"),
    ("Spain", "Spain"),
    ("Sri Lanka", "Sri Lanka"),
    ("Sudan", "Sudan"),
    ("Suriname", "Suriname"),
    ("Svalbard", "Svalbard"),
    ("Swaziland", "Swaziland"),
    ("Sweden", "Sweden"),
    ("Switzerland", "Switzerland"),
    ("Syria", "Syria"),
    ("Taiwan", "Taiwan"),
    ("Tajikistan", "Tajikistan"),
    ("Tanzania", "Tanzania"),
    ("Thailand", "Thailand"),
    ("Timor - Leste", "Timor - Leste"),
    ("Togo", "Togo"),
    ("Tokelau", "Tokelau"),
    ("Tonga", "Tonga"),
    ("Transnistria Pridnestrovie", "Transnistria Pridnestrovie"),
    ("Trinidad and Tobago", "Trinidad and Tobago"),
    ("Tristan da Cunha", "Tristan da Cunha"),
    ("Tunisia", "Tunisia"),
    ("Turkey", "Turkey"),
    ("Turkmenistan", "Turkmenistan"),
    ("Turks and Caicos Islands", "Turks and Caicos Islands"),
    ("Tuvalu", "Tuvalu"),
    ("Uganda", "Uganda"),
    ("Ukraine", "Ukraine"),
    ("United Arab Emirates", "United Arab Emirates"),
    ("United Kingdom", "United Kingdom"),
    ("United States", "United States"),
    ("Uruguay", "Uruguay"),
    ("Uzbekistan", "Uzbekistan"),
    ("Vanuatu", "Vanuatu"),
    ("Vatican City", "Vatican City"),
    ("Venezuela", "Venezuela"),
    ("Vietnam", "Vietnam"),
    ("British Virgin Islands", "British Virgin Islands"),
    ("Isle of Man", "Isle of Man"),
    ("US Virgin Islands", "US Virgin Islands"),
    ("Wallis and Futuna", "Wallis and Futuna"),
    ("Western Sahara", "Western Sahara"),
    ("Yemen", "Yemen"),
    ("Zambia", "Zambia"),
    ("Zimbabwe", "Zimbabwe"),
)


FEEDBACK_SERVICE = (
    (
        'Very satisfied',
        _('Very satisfied')
    ),
    (
        'Satisfied',
        _('Satisfied')
    ),
    (
        'Neither satisfied or dissatisfied',
        _('Neither satisfied or dissatisfied', )
    ),
    (
        'Dissatisfied',
        _('Dissatisfied')
    ),
    (
        'Very dissatisfied',
        _('Very dissatisfied')
    )
)

STAFF_CHOICES = (
    (
        'Less than 10',
        _('Less than 10')
    ),
    (
        '10 to 50',
        _('10 to 50')
    ),
    (
        '51 to 250',
        _('51 to 250')
    ),
    (
        'More than 250',
        _('More than 250')
    ),
)


class ContactForm(forms.Form):
    action_class = EmailAction

    name = fields.CharField(label=_('Name'))
    job_title = fields.CharField(label=_('Job title'))
    email = fields.EmailField(label=_('Email address'))
    phone_number = fields.CharField(
        label=_('Phone number'),
        required=True
    )
    company_name = fields.CharField(label=_('Company name'))
    company_website = fields.CharField(
        label=_('Company website'),
        required=False
    )
    country = fields.ChoiceField(
        label=_('Which country are you based in?'),
        help_text=_(
            'We will use this information to put you in touch with '
            'your closest British embassy or high commission.'),
        choices=(('', ''),) + COUNTRIES,
        widget=Select(attrs={'id': 'js-country-select'})
    )
    staff_number = fields.ChoiceField(
        label=_('Current number of staff'),
        choices=STAFF_CHOICES
    )
    description = fields.CharField(
        label=_('Tell us about your investment'),
        help_text=_(
            'Tell us about your company and your plans for the UK in '
            'terms of size of investment, operational and recruitment '
            'plans. Please also tell us what help you would like from '
            'the UK government.'
            ),
        widget=Textarea()
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )

    def __init__(self, utm_data, submission_url, *args, **kwargs):
        self.utm_data = utm_data
        self.submission_url = submission_url
        super().__init__(*args, **kwargs)

    def get_context_data(self):
        data = self.cleaned_data.copy()
        return {
            'form_data': (
                (_('Name'), data['name']),
                (_('Email address'), data['email']),
                (_('Job title'), data['job_title']),
                (_('Phone number'), data['phone_number']),
                (_('Company name'), data['company_name']),
                (_('Company website'), data.get('company_website', '')),
                (_('Country'), data['country']),
                (_('Current number of staff'), data['staff_number']),
                (_('Your investment'), data['description'])
            ),
            'utm': self.utm_data,
            'submission_url': self.submission_url,
        }

    def render_email(self, template_name):
        context = self.get_context_data()
        return render_to_string(template_name, context)

    def send_agent_email(self):
        action = self.action_class(
            recipients=[settings.IIGB_AGENT_EMAIL],
            subject='Contact form agent email subject',
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=self.submission_url,
        )
        response = action.save({
            'text_body': self.render_email('email/email_agent.txt'),
            'html_body': self.render_email('email/email_agent.html'),
        })
        response.raise_for_status()

    def send_user_email(self):
        action = self.action_class(
            recipients=[self.cleaned_data['email']],
            subject=str(_('Contact form user email subject')),
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            form_url=self.submission_url,
        )
        response = action.save({
            'text_body': self.render_email('email/email_user.txt'),
            'html_body': self.render_email('email/email_user.html'),
        })
        response.raise_for_status()

    def save(self):
        self.send_agent_email()
        self.send_user_email()
