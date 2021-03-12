from rest_app.shared import db


class AccessToken(db.Model):
    token = db.Column(db.LargeBinary)
    nonce = db.Column(db.LargeBinary)

    __table_args__ = db. PrimaryKeyConstraint('token', 'nonce'), {}
