from typing import Any, Dict

from rest_app.shared import db
from rest_app.models.product import Product


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    offer_service_id = db.Column(db.Integer, index=True)
    price = db.Column(db.Integer, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)
    added = db.Column(db.DateTime, nullable=False)
    removed = db.Column(db.DateTime)

    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product = db.relationship(Product, back_populates="offers")

    def serialize(self) -> Dict[str, Any]:
        return {
            'price': self.price,
            'items_in_stock': self.items_in_stock,
            'added': str(self.added),
            'removed': None if self.removed is None else str(self.removed),
        }
