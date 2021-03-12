from datetime import datetime
from flask import current_app
from sqlalchemy.orm import joinedload

from rest_app.models import Offer, Product
from rest_app.shared import add_scheduler_context, db, scheduler
from rest_app.services import offer_microservice


@add_scheduler_context
def refresh_offers() -> None:
    """Update the internal information based on the external offer microservice"""

    current_app.logger.info("Refreshing offers")
    products = Product.query.options(joinedload(Product.offers))

    new_offers = list()
    for product in products:
        # List of offers that is active and we did not see them in the response (at the start all not removed offers
        # will be assigned to the variable and then removed once they are seen in the response)
        unprocessed_active_offers = {offer.offer_service_id: offer for offer in product.offers if offer.removed is None}

        try:
            offer_data = offer_microservice.query_product_offers(product.id)
        except offer_microservice.OfferServiceError:
            current_app.logger.error(f'Failed to get offers for product with id={product.id!r}')
            continue

        for offer in offer_data:
            id_, price, items_in_stock = map(int, [offer['id'], offer['price'], offer['items_in_stock']])

            if id_ in unprocessed_active_offers:
                active_offer = unprocessed_active_offers[id_]
                del unprocessed_active_offers[id_]
                if active_offer.price == price and active_offer.items_in_stock == items_in_stock:
                    continue
                current_app.logger.info(f"Refreshing offer {active_offer.offer_service_id!r}")

            current_app.logger.info(f"Processing new offer for id {id_!r}")
            new_offers.append(Offer(
                offer_service_id=id_, price=price, items_in_stock=items_in_stock,
                product_id=product.id, added=datetime.now(), removed=None,
            ))

        for active_offer in unprocessed_active_offers.values():
            current_app.logger.info(f"Removing offer {active_offer.offer_service_id!r}")
            active_offer.removed = datetime.now()

    db.session.bulk_save_objects(new_offers)
    db.session.commit()


def schedule_refresh() -> None:
    scheduler.add_job(
        'offer_refresh',
        func=refresh_offers,
        trigger="interval",
        seconds=current_app.config['OFFER_REFRESH_RATE_SECONDS'],
        next_run_time=datetime.now(),
    )
    current_app.logger.info("Scheduled refreshing offer")
