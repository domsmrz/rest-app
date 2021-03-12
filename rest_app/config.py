import os


OFFER_MICROSERVICE_URI = os.getenv("OFFERS_MS_URI", "https://applifting-python-excercise-ms.herokuapp.com/api/v1")
OFFER_REFRESH_RATE_SECONDS = 60
SECRET_KEY = b'\xf3u\x8f~\xbf\x91\x05\x03\x851@\x8b\xa0\xf6\xb8Y'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:////tmp/data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
