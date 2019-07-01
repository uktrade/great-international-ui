from captcha.fields import ReCaptchaField
from django.utils.translation import ugettext_lazy as _
from django.forms import TextInput

from directory_components import forms, fields
from django_countries.data import COUNTRIES


class PerfectFitProspectusForm(forms.Form):
    name = fields.CharField(
        required=True,
        label=_('Name'),
    )
    company = fields.CharField(
        required=True,
        label=_('Company'),
    )

    email = fields.EmailField(
        required=True,
        label=_('Email'),
    )

    phone_number = fields.CharField(
        required=False,
        label=_('Phone number (optional)'),
        widget=TextInput(attrs={'type': 'tel'})
    )

    country = fields.ChoiceField(
        required=True,
        label=_('Country'),
        choices=sorted(
            [(k, v) for k, v in COUNTRIES.items()],
            key=lambda tup: tup[1]
        )
    )

    gdpr_optin = fields.BooleanField(
        label=_('I would like to receive further information.'),
        initial=False,
        required=False
    )

    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )

    def __init__(self, sector_choices, country_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sector'] = fields.ChoiceField(
            label='Sector',
            choices=sector_choices
        )
        self.fields['country'] = fields.ChoiceField(
            label='Country',
            choices=country_choices
        )
