import os

DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db:5432/{os.getenv('DB_NAME')}"
checkRate_MAX_REQUESTS = 10
checkRate_WINDOW_SECONDS = 60