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

    response = requests.post(url=f'{base_url_account_api}/Login', data=payload)
    body_token = response.json().get("token")
    token = f"Bearer {body_token}"
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

    response = requests.post(url=f'{base_url_account_api}Login', data=payload)
    userId = response.json().get("userId")
    return userId


def add_some_book_api(quantity):
    isbnArray = ["9781449325862", "9781449331818", "9781449337711", "9781449365035", "9781491904244", "9781491950296",
                 "9781593275846", "9781593277574"]
    new_collectionOfIsbns = []
    for i in range(quantity):
        d = dict.fromkeys(['isbn'], isbnArray[i])
        new_collectionOfIsbns.append(d)

    payload = json.dumps({
        "userId": get_data_userId(),
        "collectionOfIsbns": new_collectionOfIsbns
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': get_data_auth_token()
               }
    requests.post(url=f'{base_url_book_store}Books', data=payload, headers=headers)


def delete_all_books_api():
    url_with_params = f"{base_url_book_store}Books?UserId={get_data_userId()}"
    headers = {'Content-Type': 'application/json',
               'Authorization': get_data_auth_token()
               }
    requests.delete(url=url_with_params, headers=headers)
