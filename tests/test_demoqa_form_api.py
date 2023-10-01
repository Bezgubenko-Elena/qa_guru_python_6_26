from jsonschema.validators import validate
import json
import os
from data.users import Book
from tests.conftest import path_schema, base_url, base_url_book_store
from utils import helper




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


def test_create_user():
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    response = helper.reqres_api(method='post', url='/api/users', data=payload)

    assert response.status_code == 201


def test_update_user_put():
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }
    response = helper.reqres_api(method='put', url='/api/users/2', data=payload)

    assert response.status_code == 200
    assert response.json()["job"] == payload.get("job")


def test_delete_user():
    response = helper.reqres_api(method='delete', url='/api/users/2')

    assert response.status_code == 204


def test_register_successful():
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = helper.reqres_api(method='post', url='/api/register', data=payload)

    assert response.status_code == 200
    assert type(response.json()["token"] == "str")


def test_register_unsuccessful():
    payload = {
        "email": "sydney@fife"
    }
    response = helper.reqres_api(method='post', url='/api/register', data=payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_login_successful():
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = helper.reqres_api(method='post', url='/api/login', data=payload)

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_unsuccessful():
    payload = {
        "email": "peter@klaven"
    }
    response = helper.reqres_api(method='post', url='/api/login', data=payload)

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
