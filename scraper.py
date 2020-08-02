# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 22:13:29 2020

@author: saipr
"""
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

#Scrape The list of names / characters
site= "https://fedatamine.com/en-us/characters/0/Byleth/supports"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page)
names = list()
boxes = list(soup.find_all("div", {"class": "col-sm-4 col-6 col-xl-2 text-center py-2"}))
for n in range(0, len(boxes)):
    names.append(boxes[n].find("a").contents[2])  
# print(names)
# print(len(names))

#build a link list
links = list()
for n in names:
    links.append(("https://fedatamine.com/en-us/supports/"+ n ))
# print(links)
# print(len(links))

def convoScraper(charLink, fromm):
    #pull up the link
    edges = list()
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(charLink,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)

    #scrape every box
    boxes = list(soup.find_all("div", {"class": "col-sm-4 col-6 col-xl-2 text-center py-2"}))
    #build an edge between the individual and their 
    for b in boxes:
        links = b.find_all("a")
        to = links[0].contents[2]
        strength = (len(links) - 1)
        if (to != "Byleth"):
            edges.append(tuple((fromm, to, strength)))
        
    return edges

#build the edgelist
edgeList = list()
count = 0
for l in links:
    try:
        edges = convoScraper(l, names[count])
        for (t, f, n) in edges:
            if ((t, f, n) not in edgeList) and ((f, t, n) not in edgeList):
                edgeList.append((t, f, n))
        print(count, names[count])
    except:
        pass
    count +=1

#export the edgelist
dataset = pd.DataFrame(edgeList)
dataset.to_csv(r"edgeList.csv")            