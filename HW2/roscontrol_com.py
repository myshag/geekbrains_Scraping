import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = "https://roscontrol.com"
parameters = {
    "sort_val": "desc",
    "sort": "rating"
}

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

target = "/category/produkti/riba_i_moreprodukti/ribnie_konservi/"
results = requests.get(url+target, params=parameters, headers=headers)

print(results.url)
with open("output_roscontrol.com.html", "w") as output:
    print(results.text, file=output)

dom = BeautifulSoup(results.text, 'html.parser')

list__items = dom.findAll("div", attrs={"class": "wrap-product-catalog__item"})

for item in list__items:
    print(item.text)
