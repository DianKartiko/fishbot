# run.py

from bot.main import start_bot
from database.db import create_tables

if __name__ == "__main__":
    create_tables()
    start_bot()
