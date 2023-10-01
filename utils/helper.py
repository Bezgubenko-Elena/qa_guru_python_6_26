import json
import allure
import requests
from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType

from data.users import User
from tests.conftest import base_url_book_store, base_url_account_api


def book_api(method, url, **kwargs):
    new_url = base_url_book_store + url
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


def account_api(method, url, **kwargs):
    new_url = base_url_account_api + url
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

def get_data_auth_token():
        # user1 = User(
        #     user_name='ivan',
        #     password='Qq!12345'
        # )

        payload = {
            "userName": "ivan",
            "password": "Qq!12345"
        }

        response = account_api(method='post', url='Login', data=payload)
        body_token = response.json().get("token")
        token = f"Bearer {body_token}"
        # userId = response.json().get("userId")
        # assert response.status_code == 200
        # print(token, userId)
        # for text in response.json().items():
        #     print(text)
        return token


def get_data_userId():
    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    payload = {
        "userName": user1.user_name,
        "password": user1.password
    }

    response = account_api(method='post', url='Login', data=payload)
    # token = response.json().get("token")
    userId = response.json().get("userId")
    # assert response.status_code == 200
    # print(token, userId)
    # for text in response.json().items():
    #     print(text)
    return userId

def save_data_auth():
    pass