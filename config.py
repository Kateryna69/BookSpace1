import os
from dotenv import load_dotenv

load_dotenv()

DBNAME = os.getenv("DBNAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")

SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True