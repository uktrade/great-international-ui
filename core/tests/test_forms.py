from core import forms


def test_company_search_form_page_present():
    form = forms.OpportunitySearchForm(data={
        'q': 'foo',
        'page': 5,
    })
    assert form.is_valid()
    assert form.cleaned_data['page'] == 5


def test_company_search_form_page_missing():
    form = forms.OpportunitySearchForm(data={
        'q': 'foo',
    })
    assert form.is_valid()
    assert form.cleaned_data['page'] == 1
