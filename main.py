import sqlite3
import requests
import time

STAFF_DOWNLOAD_URL = "https://staff-lookup.api.nottingham.ac.uk/person-search/v1/staff/_"
DATABASE = "modules.db"


def store_result(result, db_cursor):
    db_cursor.execute("INSERT OR IGNORE INTO staff VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
        result["_username"],
        result["_salutation"],
        result["_givenName"].title(),
        result["_surname"].title(),
        result["_department"],
        result["_jobTitle"],
        result["_email"],
        int(time.time())
    ))


print("Getting staff...")

response = requests.get(STAFF_DOWNLOAD_URL)
results = response.json()["results"]

print("Saving...")

db = sqlite3.connect(DATABASE)
cursor = db.cursor()

for result in results:
    store_result(result, cursor)

db.commit()
db.close()

print("Done.")
