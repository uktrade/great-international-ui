from core.header_config.helpers import NavItem
from django.utils.translation import gettext_lazy as _
from directory_constants import urls

ABOUT_UK = NavItem(
    name='about-uk',
    title=_('About the UK'),
    url=urls.international.ABOUT_UK_HOME
)

EXPAND = NavItem(
    name='expand',
    title=_('Expand to the UK'),
    url=urls.international.EXPAND_HOME
)

INVEST_CAPITAL = NavItem(
    name='invest-capital',
    title=_('Invest capital in the UK'),
    url=urls.international.CAPITAL_INVEST_HOME
)

TRADE = NavItem(
    name='trade',
    title=_('Buy from the UK'),
    url=urls.international.TRADE_HOME
)

ABOUT_DIT = NavItem(
    name='about-us',
    title=_('About us'),
    url=urls.international.ABOUT_DIT_HOME
)
