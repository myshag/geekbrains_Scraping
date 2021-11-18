# https://hh.ru/search/vacancy?L_profession_id=5.2&area=113&no_magic=true&text=&hhtmFromLabel=rainbow_profession&
# customDomain=1
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from pymongo import MongoClient
from pprint import pprint


url = "https://hh.ru"
parameters = {
    "L_profession_id": "5.2",  # required  parameter for search  results
    "area": "113",  # default area to search
    "no_magic": "true",
    "text": "Продавец-кассир",
    "hhtmFromLabel": "rainbow_profession",
    "customDomain": "1",
    "page":0
}

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}


def getBD(bdname:str,ip:str="127.0.0.1",port:int=27017):
    client = MongoClient(ip, port)
    return client[bdname]

def parse(pageDOM):
    columnWithVacancy = dom.find("div", attrs={"class": "vacancy-serp"})
    vacancy_items = columnWithVacancy.findAll("div", attrs={"class": "vacancy-serp-item"})
    results_list = []  # list of results


    for item in vacancy_items:
        el = {}
        bloko_links = item.findAll("a", attrs={"class": "bloko-link"})
        vacancyName = bloko_links[0]  # Получаем название вакансии
        employer_name = bloko_links[1]  # Получаем название фирмы
        address = item.find("div", attrs={"data-qa": "vacancy-serp__vacancy-address"})
        responsibility = item.find("div", attrs={"data-qa": "vacancy-serp__vacancy_snippet_responsibility"})
        requirements = item.find("div", attrs={"data-qa": "vacancy-serp__vacancy_snippet_requirement"})
        compensation = item.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})

        # el['vacancyName'] = vacancyName.text
        # el['employer_name'] = employer_name.text
        # el['employer_link'] = url+employer_name.attrs['href']
        # el['employer_HHid'] = int(employer_name.attrs['href'].split("/")[2])

        # el['address'] = address.text
        # el['responsibility'] = responsibility.text
        # compensation_arr = str("".join(compensation.text.split()))

        el['compensation'] = compensation

        if not el['compensation'] is None:
            el['compensation'] = el['compensation'].replace("\u202f", "")

        # el['compensation'] = compensation_arr.split("от")

        # if requirements is not None:
        #     el['requirements'] = requirements.text
        # else:
        #     el['requirements'] = None

        results_list.append(el)
    return results_list

while True:
    result = requests.get(url + "/search/vacancy", params=parameters, headers=headers)

    with open(f"output{parameters['page']}.html", "w", encoding='utf-8') as output:
        print(result.text, file=output)

    print(f"Parsing page: {parameters['page']}")
    dom = BeautifulSoup(result.text, 'html.parser')
    pageNextButton = dom.find("a", attrs={"class": "bloko-button","data-qa":"pager-next"})

    vacancy_list_dict = parse(dom)
    dbVacancy_list


    if pageNextButton is None:
        break
    parameters['page'] += 1



#pprint(results_list)

print()
