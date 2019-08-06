from django.forms import Select
from django.utils.translation import ugettext as _

from directory_components import forms
from directory_constants import choices


class SearchForm(forms.Form):

    term = forms.CharField(
        max_length=255,
        required=False,
    )
    industries = forms.ChoiceField(
        required=False,
        choices=(
            (('', _('All industries')),) + choices.INDUSTRIES
        ),
        widget=Select(attrs={'dir': 'ltr'})
    )
