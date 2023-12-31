import json
import allure
import requests
from requests import sessions
from curlify import to_curl
from allure_commons.types import AttachmentType

from utils.class_instances import registered_user

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


def login_api_new():
    payload = {
        "userName": registered_user.user_name,
        "password": registered_user.password
    }
    data_for_return = {}
    response_token = requests.post(url=f'{base_url_account_api}GenerateToken', data=payload)
    generate_token = response_token.json().get('token')
    data_for_return['generate_token'] = generate_token

    response_id = requests.post(url=f'{base_url_account_api}Login', data=payload)
    user_id = response_id.json().get('userId')
    data_for_return['user_id'] = user_id

    return data_for_return


@allure.step("Создаем пользователя перед тестом через api")
def create_user():
    payload = {
        "userName": registered_user.user_name,
        "password": registered_user.password
    }
    requests.post(url=f'{base_url_account_api}User', data=payload)


@allure.step("Удаляем пользователя после теста через api")
def delete_user():
    user_id_and_generate_token = login_api_new()
    url_with_id = f"{base_url_account_api}User/{user_id_and_generate_token.get('user_id')}"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {user_id_and_generate_token.get("generate_token")}'
               }
    requests.delete(url=url_with_id, headers=headers)


@allure.step("Добавляем несколько книг в корзину через api")
def add_some_book_api(quantity):
    user_id_and_generate_token = login_api_new()
    isbn_dict = {0: "9781449325862", 1: "9781449331818", 2: "9781449337711", 3: "9781449365035", 4: "9781491904244",
                 5: "9781491950296", 6: "9781593275846", 7: "9781593277574"}
    new_collection_of_isbn = []
    for i in range(quantity):
        d = dict.fromkeys(['isbn'], isbn_dict[i])
        new_collection_of_isbn.append(d)

    payload = json.dumps({
        "userId": user_id_and_generate_token.get('user_id'),
        "collectionOfIsbns": new_collection_of_isbn
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {user_id_and_generate_token.get("generate_token")}'
               }
    requests.post(url=f'{base_url_book_store}Books', data=payload, headers=headers)

    return user_id_and_generate_token


@allure.step("Удаляем все книги из корзины через api")
def delete_all_books_api():
    user_id_and_generate_token = login_api_new()
    url_with_params = f"{base_url_book_store}Books?UserId={user_id_and_generate_token.get('user_id')}"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {user_id_and_generate_token.get("generate_token")}'
               }
    requests.delete(url=url_with_params, headers=headers)


def get_count_books_from_user():
    user_id_and_generate_token = login_api_new()
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {user_id_and_generate_token.get("generate_token")}'
               }
    response = requests.get(url=f"{base_url_account_api}User/{user_id_and_generate_token.get('user_id')}",
                            headers=headers)

    return len(response.json().get('books'))
