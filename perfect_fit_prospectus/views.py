import boto3
from botocore.exceptions import ClientError

from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from perfect_fit_prospectus.forms import PerfectFitProspectusForm
from directory_components.mixins import CountryDisplayMixin

from pir_client.client import pir_api_client


class PerfectFitProspectusMainView(
    CountryDisplayMixin, SuccessMessageMixin, FormView
):
    form_class = PerfectFitProspectusForm
    template_name = 'perfect_fit_prospectus/index.html'
    success_url = reverse_lazy('perfect_fit_prospectus:success')
    success_message = _(
        'Thank You. Your Perfect Fit Prospectus has been emailed to %(email)s'
    )

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


class PerfectFitProspectusSuccessView(TemplateView):
    template_name = 'perfect_fit_prospectus/success.html'


class PerfectFitProspectusReportProxyView(CountryDisplayMixin, View):
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
