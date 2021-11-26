import requests
from lxml import html
from pprint import pprint

def parse_news(url:str,headers:dict):
    res = requests.get(url, headers=headers)
    if res.ok:
        root = html.fromstring(res.text)
        date_tag = root.xpath("//span[@datetime]")[0]
        date = date_tag.attrib["datetime"]
        name = root.xpath("//h1/text()")[0]
        source =  root.xpath("//a[@class ='link color_gray breadcrumbs__link']/"
                             "span[@ class ='link__text']")
        if len(source)==1:
            source = source[0].text
        return {
            "url": url,
            "date":date,
            "name": name,
            "source":source
        }
    return None



