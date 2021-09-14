import os
from overseed.utils import delete_and_create_db
from app import app

with app.app_context():
    delete_and_create_db()

print("Finished creating database.")
