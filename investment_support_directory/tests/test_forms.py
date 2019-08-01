from directory_constants import choices, expertise
import pytest

from investment_support_directory import forms


prefix = 'expertise_products_services'

expertise_products_services_fields = [
    f'{prefix}_management',
    f'{prefix}_human_resources',
    f'{prefix}_legal',
    f'{prefix}_publicity',
    f'{prefix}_business_support'
]


def test_company_search_form_expertise_products_services():
    form = forms.CompanySearchForm(data={
        'term': 'foo',
        f'{prefix}_management': [expertise.MANAGEMENT_CONSULTING[0]],
        f'{prefix}_human_resources': [expertise.HUMAN_RESOURCES[0].replace(
            ' ', '-')
        ],
        f'{prefix}_legal': [expertise.LEGAL[0]],
        f'{prefix}_publicity': [expertise.PUBLICITY[0]],
        f'{prefix}_business_support': [expertise.BUSINESS_SUPPORT[0]],
    })
    assert form.is_valid()
    assert form.cleaned_data['expertise_products_services_labels'] == [
        expertise.MANAGEMENT_CONSULTING[0],
        expertise.HUMAN_RESOURCES[0],
        expertise.LEGAL[0],
        expertise.PUBLICITY[0],
        expertise.BUSINESS_SUPPORT[0],
    ]
    for field_name in expertise_products_services_fields:
        assert field_name in form.cleaned_data


def test_company_search_form_clean_human_resources_for_waf_error_403():
    form = forms.CompanySearchForm(data={
        f'{prefix}_human_resources': [
            expertise.HUMAN_RESOURCES[0].replace(' ', '-'),
            expertise.HUMAN_RESOURCES[6].replace(' ', '-'),
        ],
    })
    assert form.is_valid()
    field_name = 'expertise_products_services_labels'
    assert form.cleaned_data[field_name] == (
        [
            expertise.HUMAN_RESOURCES[0].replace('-', ' '),
            expertise.HUMAN_RESOURCES[6].replace('-', ' '),
        ]
    )


def test_company_search_form_page_present():
    form = forms.CompanySearchForm(data={
        'q': 'foo',
        'page': 5,
    })
    assert form.is_valid()
    assert form.cleaned_data['page'] == 5


def test_company_search_form_page_missing():
    form = forms.CompanySearchForm(data={
        'q': 'foo',
    })
    assert form.is_valid()
    assert form.cleaned_data['page'] == 1


@pytest.mark.parametrize('data', (
    {'expertise_industries': [choices.INDUSTRIES[0][0]]},
    {'expertise_regions': [choices.EXPERTISE_REGION_CHOICES[0][0]]},
    {'expertise_countries': [choices.COUNTRY_CHOICES[0][0]]},
    {'expertise_languages': [choices.EXPERTISE_LANGUAGES[0][0]]},
    {'q': 'foo'},
    {f'{prefix}_management': [expertise.MANAGEMENT_CONSULTING[0]]},
    {
        f'{prefix}_human_resources': [
            expertise.HUMAN_RESOURCES[0].replace(' ', '-')
        ]
    },
    {f'{prefix}_legal': [expertise.LEGAL[0]]},
    {f'{prefix}_publicity': [expertise.PUBLICITY[0]]},
    {f'{prefix}_business_support': [expertise.BUSINESS_SUPPORT[0]]},
    {f'{prefix}_financial': [expertise.FINANCIAL[0]]},
))
def test_minimum_viable_search(data):
    form = forms.CompanySearchForm(data=data)
    assert form.is_valid()
