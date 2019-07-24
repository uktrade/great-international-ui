from django.urls import reverse


def test_google_campaign_middleware(client):
    url = reverse('index')
    client.get(
        url,
        {
            'utm_source': 'test_source',
            'utm_medium': 'test_medium',
            'utm_campaign': 'test_campaign',
            'utm_term': 'test_term',
            'utm_content': 'test_content'
        })

    correct_utm = {
        'utm_source': 'test_source',
        'utm_medium': 'test_medium',
        'utm_campaign': 'test_campaign',
        'utm_term': 'test_term',
        'utm_content': 'test_content'
    }

    assert 'utm' in client.session
    assert client.session['utm'] == correct_utm
