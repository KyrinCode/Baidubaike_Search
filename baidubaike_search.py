# -*- coding: utf-8 -*-

import re
import bs4
import requests
from bs4 import BeautifulSoup
import sys

def getHTMLtext(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error"

def search(html, search_item):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find('div', class_="lemma-summary").children
        print("search result:")
        for x in text:
            word = re.sub(re.compile(r"<(.+?)>"),'',str(x))
            words = re.sub(re.compile(r"\[(.+?)\]"),'',word)
            print(words,'\n')
    except AttributeError:
        print("Failed!Please enter more in details!")
    else:
        polysemant = soup.find('div', class_='before-content')
        if polysemant:
            candidates = {}
            polysemant_list = polysemant.find_all('li', class_='item')
            for item in polysemant_list[1:]:
                name = item.find('a').string
                href = item.find('a').get('href')
                candidates[name] = href
            polysemant_case(candidates, search_item)

def poly_search(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('div', class_="lemma-summary").children
    print("search result:")
    for x in text:
        word = re.sub(re.compile(r"<(.+?)>"),'',str(x))
        words = re.sub(re.compile(r"\[(.+?)\]"),'',word)
        print(words,'\n')

def polysemant_case(candidates, search_item):
    if candidates:
        polyflag = input(search_item + "is a polysemant.\nIf this is not the meaning you want, press 'p': ")
        if polyflag == 'p':
            count = 0
            for k in candidates.keys():
                count += 1
                print(("{0:^3}. " + k).format(count))
            polynum = int(input("choose the number: "))
            count = 0
            for k in candidates.keys():
                count += 1
                if count == polynum:
                    meaning = k
                    poly_search(getHTMLtext('https://baike.baidu.com' + candidates[meaning]))
                    break

if __name__ == "__main__":
    search_item = input("Enter what you want ('q' to exit): ")
    if search_item == 'q':
        exit(0)
    print("please wait...")

    url = 'https://baike.baidu.com/item/' + search_item
    html = getHTMLtext(url)
    search(html, search_item)
