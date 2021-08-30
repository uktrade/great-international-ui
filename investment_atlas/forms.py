from directory_components import forms
from django.forms import Select


class InvestmentOpportunitySearchForm(forms.Form):
    # NB: There was an earlier version of this form in core.forms,
    # but this one is specific to Investment Atlas

    sector = forms.ChoiceField(
        label='sector',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-sector'},
            use_nice_ids=True,
        ),
        required=False
    )
    scale = forms.ChoiceField(
        label='scale',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-scale'},
            use_nice_ids=True,
        ),
        required=False
    )
    region = forms.ChoiceField(
        label='region',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-region'},
            use_nice_ids=True,
        ),
        required=False
    )
    sub_sector = forms.ChoiceField(
        label='sub_sector',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-sub_sector'},
            use_nice_ids=True,
        ),
        required=False
    )
    planning_status = forms.ChoiceField(
        label='planning_status',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-planning_status'},
            use_nice_ids=True,
        ),
        required=False
    )
    investment_type = forms.ChoiceField(
        label='investment_type',
        widget=forms.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-investment_type'},
            use_nice_ids=True,
        ),
        required=False
    )
    sort_by = forms.ChoiceField(
        label='sort_by',
        widget=Select(
            attrs={
                'onchange': 'this.form.submit()'
            }
        ),
        required=False,
    )

    def __init__(
            self,
            sectors,
            scales,
            regions,
            sort_by_options,
            sub_sectors,
            planning_statuses,
            investment_types,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.fields['sector'].choices = sectors
        self.fields['scale'].choices = scales
        self.fields['region'].choices = regions
        self.fields['sort_by'].choices = sort_by_options
        self.fields['sub_sector'].choices = sub_sectors
        self.fields['planning_status'].choices = planning_statuses
        self.fields['investment_type'].choices = investment_types
