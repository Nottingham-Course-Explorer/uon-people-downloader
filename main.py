import requests
from tqdm import tqdm
import json
from departments import DEPARTMENTS

BASE_URL = "https://staff-lookup.api.nottingham.ac.uk/person-search/v1.0/uk/{}/staff/page{}"

results = []


def get_page(department_name: str, page_name: int):
    url = BASE_URL.format(department_name, page_name)
    request = requests.get(url)
    return request.json()


for department in tqdm(DEPARTMENTS):
    data = get_page(department, 1)
    results += data["results"]
    pages: int = data["meta"]["totalpages"]

    if pages > 1:
        for page in range(2, pages + 1):
            data = get_page(department, page)
            results += data["results"]


with open("output.json", "w") as file:
    file.write(json.dumps(results))
