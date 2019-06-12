from botocore.exceptions import ClientError
from django.test import TestCase
from unittest.mock import patch, MagicMock


OPTIONS_DATA = {
    "country": {
        "choices": [
            {
                "value": "AF",
                "display_name": "Afghanistan"
            },
        ]
    },
    "market": {
        "choices": [
            {
                "value": "africa",
                "display_name": "africa"
            },
            {
                "value": "canada",
                "display_name": "canada"
            }
        ]
    },
    "sector": {
        "choices": [
            {
                "value": "tech",
                "display_name": "Technology"
            },
            {
                "value": "automotive",
                "display_name": "Automotive"
            },
        ]
    }
}


class ViewTest(TestCase):

    @patch('perfect_fit_prospectus.forms.PIRAPIClient')
    def test_pir_view(self, client_instance_mock):
        client_instance_mock().get_options.return_value = OPTIONS_DATA

        valid_data = {
            'name': 'Ted',
            'company': 'Corp',
            'email': 'ted@example.com',
            'country': 'US',
            'sector': 'tech',
            'g-recaptcha-response': 'PASSED',
            'gdpr_optin': 'on'
        }

        res = self.client.get('/')
        self.assertEquals(res.status_code, 200)

        res = self.client.post('/', data=valid_data)
        self.assertEquals(res.status_code, 201)

        res = self.client.post('/', data={'name': 'Ted', })
        self.assertEquals(res.status_code, 400)

        client_instance_mock().create_report.side_effect = ValueError()
        res = self.client.post('/', data=valid_data)
        self.assertEquals(res.status_code, 500)

    @patch('perfect_fit_prospectus.views.boto3')
    def test_proxy_view(self, boto3):
        boto3.client().generate_presigned_url.return_value = (
            'http://www.example.com/test.pdf'
        )

        res = self.client.get('/reports/test.pdf')
        self.assertEquals(
            res.get('location'), 'http://www.example.com/test.pdf'
        )

        boto3.client().head_object.side_effect = ClientError(
            MagicMock(), MagicMock()
        )
        # key doesn't exist
        res = self.client.get('/reports/test.pdf')
        self.assertEquals(res.status_code, 404)
