import requests


def create_response(status_code=200, json_payload={}, content=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_payload
    response._content = content
    return response
