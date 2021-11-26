import requests
from lxml import html
from pprint import pprint

from parse_news import  parse_news

url = 'https://news.mail.ru/'
headers ={
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/95.0.4638.69 Safari/537.36"
}

answer = requests.get(url, headers=headers)

if answer.ok:
    url_list = []
    root = html.fromstring(answer.text)
    main_news = root.xpath("//a[contains(@class ,'js-topnews__item')]")

    for single_news in main_news:
        url_list.append(single_news.attrib['href'])

    main_news2 = root.xpath("//li[@class = 'list__item']/a")
    for single_news in main_news2:
        url_list.append(single_news.attrib['href'])


    table_news =  root.xpath('//div[contains(@class,"cols__inner")]')

    for item in table_news:
        news = item.xpath(".//li//a | .//a[contains(@class,'newsitem__title')]")
        for single_news in news:
            url_list.append(single_news.attrib['href'])


    news_list = list()
    for url in url_list:
        news_list.append(parse_news(url, headers))

    pprint(news_list)







