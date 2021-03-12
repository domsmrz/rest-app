from flask import jsonify, Response, current_app
from flask_restful import Resource, reqparse
import requests
from typing import Optional, Tuple

from rest_app.views.shared import api_route_resource
from rest_app.models import Product
from rest_app.shared import db
from rest_app.services import offer_microservice


_parser_product = reqparse.RequestParser()
_parser_product.add_argument('name', type=str)
_parser_product.add_argument('description', type=str)


@api_route_resource('/products/', '/products/<int:product_id>/')
class ProductApi(Resource):
    _parser = _parser_product

    def get(self, product_id: Optional[int] = None) -> Response:
        if product_id is None:
            return jsonify([product.serialize() for product in Product.query])
        product = Product.query.filter_by(id=product_id).first_or_404(f"Product with id={product_id!r} does not exists")
        return jsonify(product.serialize())

    def delete(self, product_id: int) -> Tuple[str, int]:
        product = Product.query.filter_by(id=product_id).first_or_404(f"Product with id={product_id!r} does not exists")
        db.session.delete(product)
        db.session.commit()
        return Response(status=requests.codes.no_content)

    def put(self, product_id: int) -> Response:
        args = self._parser.parse_args()
        product = Product.query.filter_by(id=product_id).first_or_404(f"Product with id={product_id!r} does not exists")

        name = args.get('name', None)
        if name is not None:
            product.name = name

        description = args.get('description', None)
        if description is not None:
            product.description = description

        db.session.commit()
        return jsonify(product.serialize())

    def post(self) -> Response:
        args = self._parser.parse_args()
        current_app.logger.info(f"Creating new product with parameters {args!r}")
        product = Product(**args)
        db.session.add(product)
        db.session.commit()
        offer_microservice.register_product(product)
        return jsonify(product.serialize())
