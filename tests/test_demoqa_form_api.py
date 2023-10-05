from jsonschema.validators import validate
import json
import os

from utils.class_instances import book_from_list_1, book_from_list_2, book_not_in_list
from tests.conftest import path_schema
from utils import helper
from utils.helper import login_api_new, add_some_book_api, get_count_books_from_user


def test_get_list_of_books():
    with open(os.path.join(path_schema, "schema_get_list_books.json")) as file:
        schema = json.loads(file.read())
        response = helper.book_api('get', 'Books')
        assert response.status_code == 200
        validate(instance=response.json(), schema=schema)


def test_get_single_book():
    with open(os.path.join(path_schema, "schema_get_single_book.json")) as file:
        schema = json.loads(file.read())
        response = helper.book_api('get', 'Book', params={"ISBN": book_from_list_1.ISBN})
        assert response.status_code == 200
        validate(instance=response.json(), schema=schema)


def test_get_single_book_not_found():
    response = helper.book_api('get', 'Book', params={"ISBN": book_not_in_list.ISBN})

    assert response.status_code == 400


def test_add_books(create_and_delete_user):
    payload = json.dumps({
        "userId": login_api_new().get('userId'),
        "collectionOfIsbns": [
            {"isbn": book_from_list_1.ISBN},
            {"isbn": book_from_list_2.ISBN
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
    quantity_books = 5
    add_some_book_api(quantity_books)
    payload = json.dumps({
        "userId": login_api_new().get('userId'),
        "isbn": book_from_list_2.ISBN
    }
    )
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Bearer {login_api_new().get('generate_token')}"
               }
    url_with_params = f"Books/{book_from_list_1.ISBN}"
    response = helper.book_api(method='put', url=url_with_params, data=payload, headers=headers)
    list_books = response.json().get('books')

    assert response.status_code == 200
    list_isbn = []
    for book in list_books:
        list_isbn.append(book.get('isbn'))
    assert book_from_list_2.ISBN in list_isbn
    assert not book_from_list_1.ISBN in list_isbn


def test_delete_single_book(create_and_delete_user):
    quantity_books = 4
    add_some_book_api(quantity_books)
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
    assert get_count_books_from_user() == quantity_books - 1


def test_delete_all_books(create_and_delete_user):
    add_some_book_api(5)
    url_with_params = f"Books?UserId={login_api_new().get('userId')}"
    headers = {'Content-Type': 'application/json',
               'Authorization': f"Bearer {login_api_new().get('generate_token')}"
               }
    response = helper.book_api('delete', url_with_params, headers=headers)
    assert response.status_code == 204
    assert not get_count_books_from_user()
