from core.header_config.helpers import NavItem
from django.utils.translation import gettext_lazy as _
from directory_constants import urls


OVERVIEW_ABOUT = NavItem(
    name='overview-about-uk',
    title=_('Overview'),
    url=urls.international.ABOUT_UK_HOME
)

WHY_CHOOSE_THE_UK = NavItem(
    name='why-choose-the-uk',
    title=_('Why choose the UK'),
    url=urls.international.ABOUT_UK_WHY_CHOOSE_UK
)

INDUSTRIES = NavItem(
    name='industries',
    title=_('Industries'),
    url=urls.international.ABOUT_UK_INDUSTRIES
)

REGIONS = NavItem(
    name='regions',
    title=_('Regions'),
    url=urls.international.ABOUT_UK_REGIONS
)

CONTACT_US_ABOUT_UK = NavItem(
    name='contact-us-about-uk',
    title=_('Contact us'),
    url=urls.international.ABOUT_UK_CONTACT
)

OVERVIEW_EXPAND = NavItem(
    name='overview-expand',
    title=_('Overview'),
    url=urls.international.EXPAND_HOME
)

HOW_TO_EXPAND = NavItem(
    name='how-to-expand',
    title=_('How to expand to the UK'),
    url=urls.international.EXPAND_HOW_TO_SETUP
)

INVESTMENT_SUPPORT_DIRECTORY = NavItem(
    name='investment-support-directory',
    title=_('Professional services'),
    url=urls.international.EXPAND_ISD_HOME
)

CONTACT_US_EXPAND = NavItem(
    name='contact-us-expand',
    title=_('Contact us'),
    url=urls.international.EXPAND_CONTACT
)

OVERVIEW_INVEST_CAPITAL = NavItem(
    name='overview-invest-capital',
    title=_('Overview'),
    url=urls.international.CAPITAL_INVEST_HOME
)

# This page does not yet exist - will 404 for now.
INVESTMENT_TYPES = NavItem(
    name='investment-types',
    title=_('Investment types'),
    url=urls.international.CAPITAL_INVEST_HOME / 'investment-types'
)

INVESTMENT_OPPORTUNITIES = NavItem(
    name='investment-opportunities',
    title=_('Investment Opportunities'),
    url=urls.international.CAPITAL_INVEST_OPPORTUNITIES
)

# This page does not yet exist - will 404 for now.
HOW_TO_INVEST_CAPITAL = NavItem(
    name='how-to-invest-capital',
    title=_('How to invest capital'),
    url=urls.international.CAPITAL_INVEST_HOME / 'how-to-invest-capital'
)

CONTACT_US_INVEST_CAPITAL = NavItem(
    name='contact-us-invest-capital',
    title=_('Contact us'),
    url=urls.international.CAPITAL_INVEST_CONTACT
)

FIND_A_SUPPLIER = NavItem(
    name='find-a-supplier',
    title=_('Find a supplier'),
    url=urls.international.TRADE_FAS
)

# This page does not yet exist - will 404 for now.
HOW_TO_TRADE = NavItem(
    name='how-to-trade',
    title=_('How to buy from the UK'),
    url=urls.international.TRADE_HOME / 'how-to-trade'
)

CONTACT_US_TRADE = NavItem(
    name='contact-us-trade',
    title=_('Contact us'),
    url=urls.international.TRADE_CONTACT
)

OVERVIEW_ABOUT_DIT = NavItem(
    name='overview-about-dit',
    title=_('Overview'),
    url=urls.international.ABOUT_DIT_HOME
)

CONTACT_US_ABOUT_DIT = NavItem(
    name='contact-us-about-dit',
    title=_('Contact us'),
    url=urls.international.ABOUT_DIT_CONTACT
)
