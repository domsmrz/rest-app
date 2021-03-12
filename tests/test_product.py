import pytest
from pytest_mock import MockFixture
import requests

import rest_app
from rest_app.services import access_token
from rest_app.services import offer_microservice


@pytest.fixture
def client(mocker: MockFixture):
    mocker.patch.object(offer_microservice, 'register_product', autospec=True, return_value=42)
    mocker.patch.object(offer_microservice, 'query_product_offers', autospec=True,
                        return_value=[{'id': '1', 'price': '200', 'items_in_stock': '10'}])
    mocker.patch.object(access_token, '_request_access_token_remotely', autospec=True, return_value='dummy_token')

    app = rest_app.create_app(
        start_background_job=False,
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
    )

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_product_post(client):
    response = client.post('/products/', data={'name': "N0", 'description': "D0"})
    assert response.status_code == requests.codes.ok

    product_data = response.json
    assert product_data['name'] == "N0"
    assert product_data['description'] == "D0"


def test_product_get(client):
    response = client.post('/products/', data={'name': "N0", 'description': "D0"})
    assert response.status_code == requests.codes.ok
    product_data = response.json

    response = client.get(f"/products/{product_data['id']}/")
    assert response.status_code == requests.codes.ok

    stored_product_data = response.json
    assert product_data == stored_product_data


def test_product_update_name(client):
    response = client.post('/products/', data={'name': "N0", 'description': "D0"})
    assert response.status_code == requests.codes.ok
    product_data = response.json

    response = client.put(f"/products/{product_data['id']}/", data={'name': 'N1'})
    product_data['name'] = 'N1'
    assert response.status_code == requests.codes.ok

    response = client.get(f"/products/{product_data['id']}/")
    assert response.status_code == requests.codes.ok

    stored_product_data = response.json
    assert product_data == stored_product_data


def test_product_update_description(client):
    response = client.post('/products/', data={'name': "N0", 'description': "D0"})
    assert response.status_code == requests.codes.ok
    product_data = response.json

    response = client.put(f"/products/{product_data['id']}/", data={'description': 'D1'})
    product_data['description'] = 'D1'
    assert response.status_code == requests.codes.ok

    response = client.get(f"/products/{product_data['id']}/")
    assert response.status_code == requests.codes.ok

    stored_product_data = response.json
    assert product_data == stored_product_data


def test_product_update_all(client):
    response = client.post('/products/', data={'name': "N0", 'description': "D0"})
    assert response.status_code == requests.codes.ok
    product_data = response.json

    response = client.put(f"/products/{product_data['id']}/", data={'name': 'N1', 'description': 'D1'})
    product_data['name'] = 'N1'
    product_data['description'] = 'D1'
    assert response.status_code == requests.codes.ok

    response = client.get(f"/products/{product_data['id']}/")
    assert response.status_code == requests.codes.ok

    stored_product_data = response.json
    assert product_data == stored_product_data


def test_product_delete(client):
    response = client.post('/products/', data={'name': "N0", 'description': "D0"})
    assert response.status_code == requests.codes.ok
    product_data = response.json

    response = client.delete(f"/products/{product_data['id']}/")
    assert response.status_code == requests.codes.no_content

    response = client.get(f"/products/{product_data['id']}/")
    assert response.status_code == requests.codes.not_found
