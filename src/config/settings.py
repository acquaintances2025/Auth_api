import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')

    SECRET_KEY = os.environ.get('KEY')
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")
    EXP_ACCESS_TOKEN = os.environ.get('EXP_ACCESS')
    EXP_REFRESH_TOKEN = os.environ.get('EXP_REFRESH')

    PSQL_DB_USER = os.environ.get("PSQL_DB_USER")
    PSQL_DB_PASSWORD = os.environ.get("PSQL_DB_PASSWORD")
    PSQL_DB_NAME = os.environ.get("PSQL_DB_NAME")
    PSQL_DB_HOST = os.environ.get("PSQL_DB_HOST")
    PSQL_DB_PORT = os.environ.get("PSQL_DB_PORT")

    MAIL_SERVICE_ADRESS = os.environ.get("MAIL_SERVICE_ADRESS")
    MAIL_SERVICE_PORT = os.environ.get("MAIL_SERVICE_PORT")
    MAIL_SERVICE_USER = os.environ.get("MAIL_SERVICE_USER")
    MAIL_SERVICE_PASS = os.environ.get("MAIL_SERVICE_PASS")

    SMS_AERO_USER = os.environ.get("SMS_AERO_USER")
    SMS_AERO_API_KEY = os.environ.get("SMS_AERO_API_KEY")
    SMS_AERO_CONFIRMATION_NUMBER = os.environ.get("SMS_AERO_CONFIRMATION_NUMBER")