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
    def __init__(
            self,
            sectors,
            scales,
            regions,
            sort_by_options,
            *args,
            **kwargs
    ):
        super(OpportunitySearchForm, self).__init__(*args, **kwargs)

        self.fields['sector'] = fields.ChoiceField(
            label=_('Sectors'),
            widget=widgets.CheckboxSelectInlineLabelMultiple(
                attrs={'id': 'checkbox-industry-expertise'},
                use_nice_ids=True,
            ),
            required=False,
            choices=sectors
        )
        self.fields['scale'] = fields.ChoiceField(
            label=_('Scale (GDV)'),
            widget=widgets.CheckboxSelectInlineLabelMultiple(
                attrs={'id': 'checkbox-industry-expertise'},
                use_nice_ids=True,
            ),
            required=False,
            choices=scales
        )
        self.fields['region'] = fields.ChoiceField(
            label=_('Region'),
            widget=widgets.CheckboxSelectInlineLabelMultiple(
                attrs={'id': 'checkbox-industry-expertise'},
                use_nice_ids=True,
            ),
            required=False,
            choices=regions
        )
        self.fields['sort_by_drop_down'] = fields.ChoiceField(
            initial='Sort by',
            label=_('sort-by-options'),
            widget=Select(),
            choices=sort_by_options,
            required=False,
        )
