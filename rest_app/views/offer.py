from datetime import date
from flask import abort, jsonify, Response
from sqlalchemy import and_, or_, cast, Date

from rest_app.views.shared import blueprint
from rest_app.models import Offer


@blueprint.route('/offers/product/<int:product_id>/from/<string:from_date_str>/to/<string:to_date_str>/')
def offer_trend(product_id: int, from_date_str: str, to_date_str: str) -> Response:
    try:
        from_date = date.fromisoformat(from_date_str)
        to_date = date.fromisoformat(to_date_str)
    except ValueError:
        abort(400, "Invalid date format")
        raise RuntimeError("Unknown internal error")  # Should not be ever reached, as abort stops the execution

    offers = Offer.query.filter(and_(
        Offer.product_id == product_id,
        cast(Offer.added, Date) <= to_date,
        or_(Offer.removed.is_(None), cast(Offer.removed, Date) >= from_date),
        Offer.items_in_stock > 0,
    )).order_by(Offer.added).all()

    price_raise = offers[-1].price / offers[0].price if offers else None
    # FIXME: There should be probably more complex evaluation
    return jsonify({
        'price_raise': price_raise,
        'offers': [o.serialize() for o in offers]
    })
