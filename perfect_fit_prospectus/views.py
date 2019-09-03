import boto3
from botocore.exceptions import ClientError

from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from directory_components import mixins
from pir_client.client import pir_api_client

from core import helpers
from core.mixins import InternationalHeaderMixin
from core.header_config import tier_one_nav_items
from perfect_fit_prospectus.forms import PerfectFitProspectusForm


class PerfectFitBaseView(
    mixins.CountryDisplayMixin,
    InternationalHeaderMixin,
    mixins.GA360Mixin
):
    header_section = tier_one_nav_items.EXPAND

    def dispatch(self, request, *args, **kwargs):
        dispatch_result = super().dispatch(request, *args, **kwargs)
        ga360_data = helpers.get_ga_data_for_page(self.page_type)
        self.set_ga360_payload(
            page_id=self.page_type,
            business_unit=ga360_data['business_unit'],
            site_section=ga360_data['site_section'],
            site_subsection=ga360_data['site_subsection']
        )
        return dispatch_result


class PerfectFitProspectusMainView(PerfectFitBaseView, SuccessMessageMixin, FormView):
    form_class = PerfectFitProspectusForm
    template_name = 'perfect_fit_prospectus/index.html'
    success_url = reverse_lazy('perfect_fit_prospectus:success')
    success_message = _(
        'Thank You. Your Perfect Fit Prospectus has been emailed to %(email)s'
    )
    page_type = 'PerfectFitFormPage'

    def form_valid(self, form):
        data = form.cleaned_data
        response = pir_api_client.create_report(data)
        response.raise_for_status()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        response = pir_api_client.get_options()
        options = response.json()['actions']['POST']

        sector_choices = [
            (sector['value'], sector['display_name'])
            for sector in options['sector']['choices']
        ]

        country_choices = [
            (country['value'], country['display_name'])
            for country in options['country']['choices']
        ]

        kwargs['sector_choices'] = sector_choices
        kwargs['country_choices'] = country_choices
        return kwargs


class PerfectFitProspectusSuccessView(PerfectFitBaseView, TemplateView):
    template_name = 'perfect_fit_prospectus/success.html'
    page_type = 'PerfectFitFormSuccessPage'


class PerfectFitProspectusReportProxyView(View):
    def get(self, request, filename):
        client = boto3.client(
            's3',
            aws_access_key_id=settings.PFP_AWS_S3_PDF_STORE_ACCESS_KEY_ID,
            aws_secret_access_key=settings.PFP_AWS_S3_PDF_STORE_SECRET_ACCESS_KEY,  # NOQA
            region_name=settings.PFP_AWS_S3_PDF_STORE_BUCKET_REGION,
        )

        try:
            client.head_object(
                Bucket=settings.PFP_AWS_S3_PDF_STORE_BUCKET_NAME, Key=filename
            )
        except ClientError:
            raise Http404

        url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.PFP_AWS_S3_PDF_STORE_BUCKET_NAME,
                'Key': filename
            },
            ExpiresIn=3600
        )

        return HttpResponseRedirect(url)
