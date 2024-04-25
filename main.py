import requests
from departments import DEPARTMENTS

BASE_URL = "https://staff-lookup.api.nottingham.ac.uk/person-search/v1.0/uk/{}/staff/page{}"

for department in DEPARTMENTS:
    print(BASE_URL.format(department, 1))


