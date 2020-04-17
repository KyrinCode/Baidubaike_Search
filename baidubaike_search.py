#!/usr/bin/env python

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
        summary = soup.find('div', class_="lemma-summary")
        if summary:
            text = summary.children
            # print("\nsearch result:")
            for x in text:
                word = re.sub(re.compile(r"<(.+?)>"),'',str(x))
                words = re.sub(re.compile(r"\[(.+?)\]"),'',word)
                print(words,'\n')
            polysemant = soup.find('div', class_='before-content')
            class_name = 'item'
            list_front = 1
        else:            
            polysemant = soup.find('ul', class_='custom_dot para-list list-paddingleft-1')
            class_name = 'list-dot list-dot-paddingleft'
            list_front = 0
    except AttributeError:
        print("\nFailed!Please enter more in details!")
    else:
        if polysemant:
            candidates = {}
            polysemant_list = polysemant.find_all('li', class_=class_name)
            for item in polysemant_list[list_front:]:
                name = item.find('a').string
                href = item.find('a').get('href')
                candidates[name] = href
            polysemant_case(candidates, search_item)
        

def poly_search(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('div', class_="lemma-summary").children
    # print("\search result:")
    for x in text:
        word = re.sub(re.compile(r"<(.+?)>"),'',str(x))
        words = re.sub(re.compile(r"\[(.+?)\]"),'',word)
        print(words,'\n')

def polysemant_case(candidates, search_item):
    if candidates:
        polyflag = input(search_item + " is a polysemant.\nIf this is not the meaning you want, press 'p': ")
        if polyflag == 'p':
            count = 0
            for k in candidates.keys():
                count += 1
                print(("{0:^3}. " + k).format(count))
            polynum = int(input("\nChoose a number: "))
            count = 0
            for k in candidates.keys():
                count += 1
                if count == polynum:
                    meaning = k
                    poly_search(getHTMLtext('https://baike.baidu.com' + candidates[meaning]))
                    break

if __name__ == "__main__":
    while(True):
        search_item = input("Search: ")
        if search_item in ["q", "exit"]:
            break
        print("\nloading...\n")

        url = 'https://baike.baidu.com/item/' + search_item
        html = getHTMLtext(url)
        search(html, search_item)
