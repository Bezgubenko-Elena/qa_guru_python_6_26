from jsonschema.validators import validate
import json
import os
from utils import helper

path_schema = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))
base_url = "https://reqres.in"


def test_get_single_user():
    response = helper.reqres_api('get', '/api/users/2')

    assert response.status_code == 200


def test_single_user_schema():
    with open(os.path.join(path_schema, "schema_single_user.json")) as file:
        schema = json.loads(file.read())
        response = helper.reqres_api('get', '/api/users/2')

        validate(instance=response.json(), schema=schema)


def test_get_single_user_not_found():
    response = helper.reqres_api('get', '/api/users/23')

    assert response.status_code == 404
    assert not len(response.json())


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
