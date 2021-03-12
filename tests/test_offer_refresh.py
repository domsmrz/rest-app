from datetime import date
import pytest
from pytest_mock import MockFixture
import requests
from time import sleep

import rest_app
from rest_app.services import access_token
from rest_app.services import offer_microservice
from rest_app.shared import scheduler


@pytest.fixture
def client(mocker: MockFixture):
    mocker.patch.object(offer_microservice, 'register_product', autospec=True, return_value=42)
    mocker.patch.object(offer_microservice, 'query_product_offers', autospec=True,
                        return_value=[{'id': '1', 'price': '200', 'items_in_stock': '10'}])
    mocker.patch.object(access_token, '_request_access_token_remotely', autospec=True, return_value='dummy_token')

    app = rest_app.create_app(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        OFFER_REFRESH_RATE_SECONDS=2,
        shutdown_scheduler=False,
    )

    with app.app_context():
        with app.test_client() as client:
            yield client

    scheduler.shutdown()


def test_offer_refresh(client):
    client.post('/products/', data={'name': "N0", 'description': "D0"})
    sleep(3)  # Waiting for background job to trigger at least once
    today = date.today().isoformat()

    response = client.get(f'/offers/product/1/from/{today}/to/{today}/')
    assert response.status_code == requests.codes.ok
    assert len(response.json['offers']) == 1
