from typing import Dict, Any

from rest_app.shared import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    offers = db.relationship("Offer")

    def serialize(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
