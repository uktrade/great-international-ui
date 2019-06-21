import boto3
from botocore.exceptions import ClientError

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.views.generic import FormView
from django.views.generic.base import View
from requests import HTTPError

from perfect_fit_prospectus.forms import PerfectFitProspectusForm
from directory_components.mixins import CountryDisplayMixin

from pir_client.client import pir_api_client


class PerfectFitProspectusMainView(CountryDisplayMixin, FormView):
    form_class = PerfectFitProspectusForm
    template_name = 'index.html'

    def form_valid(self, form):
        data = form.cleaned_data

        try:
            pir_api_client.create_report(data)
        except HTTPError:
            return render(
                self.request,
                'index.html',
                {
                    'error': (
                        'Something is wrong with the service.'
                        ' Please try again later'
                    )
                }
            )
        return render(
            self.request,
            'index.html',
            {'email': data['email']}
        )


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
