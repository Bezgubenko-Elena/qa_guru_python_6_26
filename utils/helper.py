import json
import os

import allure
import requests
from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType

from data.users import User


path_schema = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))

base_url = "https://demoqa.com"

base_url_book_store = "https://demoqa.com/BookStore/v1/"

base_url_account_api = "https://demoqa.com/Account/v1/"

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

def login_in_profile_api():
    # надо сделать через куки
    url_with_params = f"{base_url_account_api}User/{get_data_userId()}"
    headers = {'Content-Type': 'application/json',
               'Authorization': get_data_auth_token()
               }
    with allure.step('Логин через api'):
        requests.get(url_with_params, headers=headers)

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



def login_api_new():
    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    payload = {
        "userName": user1.user_name,
        "password": user1.password
    }
    data_for_return = {}
    response_token = requests.post(url=f'{base_url_account_api}GenerateToken', data=payload)
    generate_token = response_token.json().get('token')
    data_for_return['generate_token'] = generate_token


    response_id = requests.post(url=f'{base_url_account_api}Login', data=payload)
    userId = response_id.json().get('userId')
    data_for_return['userId'] = userId

    return data_for_return

def test_new_f2():
    print(login_api_new())



def create_user():
    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    payload = {
        "userName": user1.user_name,
        "password": user1.password
    }
    response = requests.post(url=f'{base_url_account_api}User', data=payload)
    uId = response.json().get('userID')
    return uId

def test_new_f1():
    print(create_user())


def delete_user():

    data_userId_and_token = login_api_new()
    url_with_id = f"{base_url_account_api}User/{data_userId_and_token.get('userId')}"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {data_userId_and_token.get("generate_token")}'
               }
    response = requests.delete(url=url_with_id, headers=headers)
    st = response.status_code
    return st

def test_new_f():
    print(delete_user())