from jsonschema.validators import validate
import json
import os

from data.users import Book
from utils.class_instances import book3, book1, book2
from tests.conftest import path_schema
from utils import helper
from utils.helper import login_api_new, add_some_book_api


def test_get_list_of_books():
    with open(os.path.join(path_schema, "schema_get_list_books.json")) as file:
        schema = json.loads(file.read())
        response = helper.book_api('get', 'Books')
        assert response.status_code == 200
        validate(instance=response.json(), schema=schema)


def test_get_single_book():

    with open(os.path.join(path_schema, "schema_get_single_book.json")) as file:
        schema = json.loads(file.read())
        response = helper.book_api('get', 'Book', params={"ISBN": book1.ISBN})
        assert response.status_code == 200
        validate(instance=response.json(), schema=schema)

def test_get_single_book_not_found():

    response = helper.book_api('get', 'Book', params={"ISBN": book3.ISBN})

    assert response.status_code == 400


def test_add_books(create_and_delete_user):
    payload = json.dumps({
        "userId": login_api_new().get('userId'),
        "collectionOfIsbns": [
            {"isbn": "9781449325862"},
            {"isbn": "9781449331818"
             }
        ]
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Bearer {login_api_new().get('generate_token')}"
               }
    response = helper.book_api(method='post', url='Books', data=payload, headers=headers)

    assert response.status_code == 201


def test_replace_single_book(create_and_delete_user):
    add_some_book_api(5)
    payload = json.dumps({
        "userId": login_api_new().get('userId'),
        "isbn": book1.ISBN
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Bearer {login_api_new().get('generate_token')}"
               }
    url_with_params = f"Books/{book2.ISBN}"
    response = helper.book_api(method='put', url=url_with_params, data=payload, headers=headers)

    assert response.status_code == 200


def test_delete_single_book(create_and_delete_user):
    add_some_book_api(4)
    payload = json.dumps({
        "isbn": "9781449325862",
        "userId": login_api_new().get('userId')
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Bearer {login_api_new().get('generate_token')}"
               }
    response = helper.book_api('delete', 'Book', data=payload, headers=headers)
    assert response.status_code == 204

    # здесь можно проверить, что остальные книги остались в корзине


def test_delete_all_books(create_and_delete_user):
    add_some_book_api(5)
    url_with_params = f"Books?UserId={login_api_new().get('userId')}"
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Bearer {login_api_new().get('generate_token')}"
               }
    response = helper.book_api('delete', url_with_params, headers=headers)
    assert response.status_code == 204
    # проверить что корзина пустая (может запросить количество книг)