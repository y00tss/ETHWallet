import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SECRET_AUTH = os.environ.get("SECRET_AUTH")
METAMASK_SECRET = os.environ.get("METAMASK_SECRET")
ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY")


DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
