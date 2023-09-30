import json
import allure
import requests
from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType
from tests.conftest import base_url


def book_api(method, url, **kwargs):
    new_url = base_url + url
    method = method.upper()
    with allure.step(f"{method} {url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)
            if response.content:
                allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"), name="Response Json",
                              attachment_type=AttachmentType.JSON, extension='json')
            else:
                allure.attach(body=message.encode("utf8"), name="Curl", attachment_type=AttachmentType.TEXT,
                              extension='txt')

    return response


def get_data_auth():
    pass


def save_data_auth():
    pass