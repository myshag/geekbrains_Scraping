import requests
from pprint import pprint
import json

org = "google"
github_url = "https://api.github.com"
end_point = f"/orgs/{org}/repos"
parameters = {
    "sort": "updated",
    "page": "4"
}


def print_respons(res):
    n = 0
    for repository in res:
        print(n := n + 1)
        print(f"Name repo: {repository.get('full_name')}")
        print(f"Description: {repository.get('description')}")
        print("-" * 20)


respons = requests.get(github_url + end_point, params=parameters)
if respons.ok:
    respons_json = respons.json()
    print_respons(respons_json)
    #Используется модуль json для человекочитаемого вывода в фыйл
    with open("outFile.json", 'w+', encoding='utf-8') as f:
        f.write(json.dumps(respons_json, indent=2))

else:
    print(f"Error, status code: {respons.status_code}")

