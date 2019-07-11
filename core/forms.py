from directory_components import forms, fields, helpers, widgets
from django.forms import Select
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.translation import ugettext_lazy as _

from directory_constants.choices import COUNTRY_CHOICES

COUNTRIES = BLANK_CHOICE_DASH + COUNTRY_CHOICES


class CountryForm(forms.Form):
    country = fields.ChoiceField(
        label='Country',
        widget=Select(attrs={'id': 'js-country-select'}),
        choices=COUNTRIES
    )


def get_country_form_initial_data(request):
    return {
        'country': helpers.get_user_country(request).upper() or None
    }


class TariffsCountryForm(forms.Form):
    tariffs_country = fields.ChoiceField(
        label='Country',
        widget=Select(attrs={'id': 'js-tariffs-country-select'}),
        choices=COUNTRIES
    )


class OpportunitySearchForm(forms.Form):

    sector = fields.ChoiceField(
        label=_('sector'),
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-sector'},
            use_nice_ids=True,
        ),
        required=False
    )
    scale = fields.ChoiceField(
        label=_('scale'),
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-scale'},
            use_nice_ids=True,
        ),
        required=False
    )
    region = fields.ChoiceField(
        label=_('region'),
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-region'},
            use_nice_ids=True,
        ),
        required=False
    )
    sort_by = fields.ChoiceField(
        label=_('sort_by'),
        widget=forms.Select(
            attrs={
                'onchange': 'this.form.submit()'
            }
        ),
        required=False,
    )

    def __init__(
            self, sectors, scales, regions,
            sort_by_options, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.fields['sector'].choices = sectors
        self.fields['scale'].choices = scales
        self.fields['region'].choices = regions
        self.fields['sort_by'].choices = sort_by_options
