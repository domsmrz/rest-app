from Crypto.Cipher import AES
import requests
from flask import current_app
from typing import Optional

from rest_app.models import AccessToken
from rest_app.shared import db


class FailedAccess(Exception):
    pass


_access_token: Optional[str] = None


def get_access_token() -> str:
    """The only public method to retrieving access token for the offer microservice"""
    global _access_token
    if _access_token is None:
        _access_token = _request_access_token()
    return _access_token


def _request_access_token() -> str:
    """Fetch the token from database (if present) or remotely"""
    current_app.logger.info("Requesting new access token...")
    secret_key = current_app.config["SECRET_KEY"]
    db_record = AccessToken.query.one_or_none()
    if db_record is not None:
        current_app.logger.info("... found one in the database")
        cipher_text, nonce = db_record.token, db_record.nonce
        cipher = AES.new(secret_key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(cipher_text).decode('ascii')

    current_app.logger.info("... no token in database, querying microservice")

    raw_token = _request_access_token_remotely()
    bytes_token = raw_token.encode('ascii')
    cipher = AES.new(secret_key, AES.MODE_EAX)

    db.session.add(AccessToken(token=cipher.encrypt(bytes_token), nonce=cipher.nonce))
    db.session.commit()
    return raw_token


def _request_access_token_remotely() -> str:
    """Obtain the token from external microservice"""
    response = requests.post(f'{current_app.config["OFFER_MICROSERVICE_URI"]}/auth')
    if not response.ok:
        raise FailedAccess
    content = response.json()
    if 'access_token' not in content:
        raise FailedAccess
    current_app.logger.info(f"Obtained access token")

    return content['access_token']
