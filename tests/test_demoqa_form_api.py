from jsonschema.validators import validate
import json
import os

from requests.auth import HTTPBasicAuth

from data.users import Book, User
from utils.helper import path_schema, base_url, base_url_book_store
from utils import helper
from utils.helper import get_data_auth_token, get_data_userId


def test_get_list_of_books():
    with open(os.path.join(path_schema, "schema_get_list_books.json")) as file:
        schema = json.loads(file.read())
        response = helper.book_api('get', 'Books')
        assert response.status_code == 200
        validate(instance=response.json(), schema=schema)


def test_get_single_book():
    book1 = Book(
        title='Git Pocket Guide',
        ISBN='9781449325862'
    )

    with open(os.path.join(path_schema, "schema_get_single_book.json")) as file:
        schema = json.loads(file.read())
        response = helper.book_api('get', 'Book', params={"ISBN": book1.ISBN})
        assert response.status_code == 200
        validate(instance=response.json(), schema=schema)


def test_get_single_book_not_found():
    book3 = Book(
        title='Book is not in Book Store',
        ISBN='0000000000000'
    )

    response = helper.book_api('get', 'Book', params={"ISBN": book3.ISBN})

    assert response.status_code == 400


def test_add_books():
    payload = json.dumps({
        "userId": get_data_userId(),
        "collectionOfIsbns": [
            {"isbn": "9781449325862"},
            {"isbn": "9781449331818"
             }
        ]
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': get_data_auth_token()
               }
    response = helper.book_api(method='post', url='Books', data=payload, headers=headers)

    assert response.status_code == 201


def test_replace_single_book():
    # сначала надо добавить книгу book2 в профиль
    book1 = Book(
        title='Git Pocket Guide',
        ISBN='9781449325862'
    )
    book2 = Book(
        title="You Don't Know JS",
        ISBN='9781491904244'
    )
    payload = json.dumps({
        "userId": get_data_userId(),
        "isbn": book1.ISBN
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': get_data_auth_token()
               }
    url_with_params = f"Books/{book2.ISBN}"
    response = helper.book_api(method='put', url=url_with_params, data=payload, headers=headers)

    assert response.status_code == 200


def test_delete_single_book():
    payload = json.dumps({
        "isbn": "9781449325862",
        "userId": get_data_userId()
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': get_data_auth_token()
               }
    response = helper.book_api('delete', 'Book', data=payload, headers=headers)
    assert response.status_code == 204

    # здесь можно проверить, что остальные книги остались в корзине


def test_delete_all_books():
    url_with_params = f"Books?UserId={get_data_userId()}"
    headers = {'Content-Type': 'application/json',
               'Authorization': get_data_auth_token()
               }
    response = helper.book_api('delete', url_with_params, headers=headers)
    assert response.status_code == 204
