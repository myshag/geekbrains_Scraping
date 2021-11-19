# https://hh.ru/search/vacancy?L_profession_id=5.2&area=113&no_magic=true&text=&hhtmFromLabel=rainbow_profession&
# customDomain=1
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime


url = "https://hh.ru"
parameters = {
    "L_profession_id": "5.2",  # required  parameter for search  results
    "area": "113",  # default area to search
    "no_magic": "true",
    #"text": "Продавец-кассир",
    "hhtmFromLabel": "rainbow_profession",
    "customDomain": "1",
    "page":0
}

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}


def getDB(bdname:str,ip:str="127.0.0.1",port:int=27017):
    client = MongoClient(ip, port)
    return client[bdname]

def readTextfromTag(domElement):
    if not domElement is None:
        return domElement.text
    else:
        return None

def parse(pageDOM:str):




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

        el['vacancyName'] = readTextfromTag(vacancyName)
        el['employer_name'] = readTextfromTag(employer_name)
        el['address'] = readTextfromTag(address)
        el['responsibility'] = readTextfromTag(responsibility)
        el['requirements'] = readTextfromTag(requirements)


        if not employer_name is None:
            el['employer_link'] = url+employer_name.attrs['href']
        else:
            el['employer_link'] = None

        if not compensation is None:
            compensation_text = compensation.text
            compensation_text = compensation_text.replace("\u202f", "")
            compensation_text = compensation_text.split()
            #print(compensation_text)
            if compensation_text[0] == 'от':
                # noinspection PyTypedDict
                el['compensation'] = {
                    "min":  int(compensation_text[1]),
                    "max": None,
                    "currency":compensation_text[2]
                }
            elif compensation_text[0] == 'до':
                # noinspection PyTypedDict
                el['compensation'] = {
                    "min": None,
                    "max": int(compensation_text[1]),
                    "currency": compensation_text[2]
                }
            elif compensation_text[0].isdigit():
                el['compensation'] = {
                    "min": int(compensation_text[0]),
                    "max": int(compensation_text[2]),
                    "currency": compensation_text[3]
                }


        results_list.append(el)
    return results_list

db=getDB("hhru_vacancy")

vacancy_name = input("Введите имя вакансии:")
parameters["text"] = vacancy_name



vacancy_collect = db[f"vacancy_collect_for {vacancy_name} in {datetime.now()}"]
vacancy_collect.insert_one(parameters)

while True:
    result = requests.get(url + "/search/vacancy", params=parameters, headers=headers)

    with open(f"output{parameters['page']}.html", "w", encoding='utf-8') as output:
        print(result.text, file=output)

    print(f"Parsing page: {parameters['page']}")
    dom = BeautifulSoup(result.text, 'html.parser')
    pageNextButton = dom.find("a", attrs={"class": "bloko-button","data-qa":"pager-next"})
    vacancy_list_dict = parse(dom)


    for vacancy in vacancy_list_dict:
        vacancy_collect.insert_one(vacancy)


    if pageNextButton is None:
        break
    parameters['page'] += 1



#pprint(results_list)

print()
