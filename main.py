import requests
from tqdm import tqdm
import json
from departments import DEPARTMENTS

BASE_URL = "https://staff-lookup.api.nottingham.ac.uk/person-search/v1.0/uk/{}/staff/page{}"

results = []

for department in tqdm(DEPARTMENTS):
    url = BASE_URL.format(department, 1)
    request = requests.get(url)
    data = request.json()
    results += data["results"]
    pages: int = data["meta"]["totalpages"]

    if pages > 1:
        for page in range(2, pages + 1):
            url = BASE_URL.format(department, page)
            request = requests.get(url)
            data = request.json()
            results += data["results"]


with open("output.json", "w") as file:
    file.write(json.dumps(results))
