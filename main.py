import sqlite3
import requests
from tqdm import tqdm
import time

STAFF_LOOKUP_BASE_URL = "https://staff-lookup.api.nottingham.ac.uk/person-search/v1.0/uk/{}/staff/page{}"
UNITS_LOOKUP_URL = "https://staff-lookup.api.nottingham.ac.uk/person-search/v1/orgunits/uk/staff"
DATABASE = "modules.db"


def get_staff_results_page(department_name: str, page_num: int):
    url = STAFF_LOOKUP_BASE_URL.format(department_name, page_num)
    request = requests.get(url)
    return request.json()


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


def store_results(results, db_cursor):
    for result in results:
        store_result(result, db_cursor)


print("Getting departments...")
departments = [result["DepartmentName"] for result in requests.get(UNITS_LOOKUP_URL).json()["results"]]

print("Getting staff...")

db = sqlite3.connect(DATABASE)
cursor = db.cursor()

for department in tqdm(departments):
    first_page = get_staff_results_page(department, 1)
    store_results(first_page["results"], cursor)
    pages: int = first_page["meta"]["totalpages"]
    
    if pages > 1:
        for i in range(2, pages + 1):
            page = get_staff_results_page(department, i)
            store_results(page["results"], cursor)

db.commit()
db.close()

print("Done.")
