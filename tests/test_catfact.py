from jsonschema.validators import validate
import json
import os
from tests.conftest import path_schema
from utils import helper




def test_get_list_breeds():
    response = helper.catfact_api('get', '/breeds')

    assert response.status_code == 200


def test_get_list_breeds_schema():
    with open(os.path.join(path_schema, "schema_breeds.json")) as file:
        schema = json.loads(file.read())
        response = helper.catfact_api('get', '/breeds')

        validate(instance=response.json(), schema=schema)


def test_get_random_fact():
    response = helper.catfact_api('get', '/fact')

    assert response.status_code == 200


def test_get_random_facts():
    response = helper.catfact_api(method='get', url='/fact')

    assert response.status_code == 200
