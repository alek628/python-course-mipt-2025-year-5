from os import getenv

DB_USERNAME = str(getenv("db_username"))
DB_PASSWORD = str(getenv("db_password"))
DB_HOST = str(getenv("db_host"))
DB_PORT = str(getenv("db_port"))
DB_NAME = str(getenv("db_name"))
SECRET_KEY = str(getenv("secret_key"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("access_token_expire_minutes"))
