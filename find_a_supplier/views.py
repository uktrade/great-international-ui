from core.views import LegacyRedirectCoreView
from . import redirects


class LegacySupplierURLRedirectView(LegacyRedirectCoreView):
    redirects_mapping = redirects.REDIRECTS
    fallback_url = '/international/trade/'
