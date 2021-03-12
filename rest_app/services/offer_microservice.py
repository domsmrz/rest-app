from flask import current_app
import requests
from typing import Dict, List

from rest_app.services.access_token import get_access_token
from rest_app.models import Product


class OfferServiceError(Exception):
    pass


def register_product(product: Product) -> None:
    current_app.logger.info(f"Registering product {product.name!r}")
    response = requests.post(
        f"{current_app.config['OFFER_MICROSERVICE_URI']}/products/register",
        headers={'Bearer': get_access_token()},
        data=product.serialize(),
    )
    if not response.ok:
        raise OfferServiceError


def query_product_offers(product_id: int) -> List[Dict[str, str]]:
    current_app.logger.info(f"Querying offers for product id={product_id!r}")
    response = requests.get(f"{current_app.config['OFFER_MICROSERVICE_URI']}/products/{product_id}/offers",
                            headers={'Bearer': get_access_token()})
    if not response.ok:
        raise OfferServiceError

    return response.json()
