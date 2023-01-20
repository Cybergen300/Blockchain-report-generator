#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 23:38:48 2023

@author: cybergenLab

functions pdf generators
"""

from bs4 import BeautifulSoup 
import requests 
from pytrends.request import TrendReq
from pygooglenews import GoogleNews
import pandas as pd


def name_formatting(var): 
    name = var.lower()
    name = name.replace(" ", "-")
    return name 

#def find_text(tag, var):
#    text = soup.find(tag, class_ = var).text
#    return text
#
#def get_Google_interest():
#    interest = pytrends.interest_over_time()
#    return interest
#
#def get_top_Google_interest(): 
#    regions = pytrends.interest_by_region(resolution= 'COUNTRY', inc_low_vol=True, inc_geo_code=False) 
#    regions.sort_values(by=[name], inplace=True, ascending=False)
#    regions= list(regions.index)
#    region1= regions[0]
#    region2= regions[1]
#    region3= regions[2]
#    region4= regions[3]
#    region5= regions[4]
#    region6= regions[5]
#    region7= regions[6]
#    region8= regions[7]
#    region9= regions[8]
#    region10= regions[9]   
#    return region1, region2, region3, region4, region5, region6, region7, region8, region9, region10
#
#def get_related_queries():
#    queries = pytrends.related_queries()
#    queries= queries[name]['top'][:10]
#    querie1= queries['query'][0]
#    querie2= queries['query'][1]
#    querie3= queries['query'][2]
#    querie4= queries['query'][3]
#    querie5= queries['query'][4]   
#    return querie1, querie2, querie3, querie4, querie5
#
#def get_titles(search): 
#    stories = []
#    search = gn.search(search, when ='6d')
#    newsitem = search['entries']
#    for item in newsitem:
#        story = {
#            'title': item.title,
#            'link' : item.link
#        }
#        stories.append(story)
#    return stories[:20]
#
#def get_top_news(name):
#    list_of_dfs= list()
#    keyword = name + " news"
#
#    #Data Gathering
#    feed = get_titles(keyword)
#    df = pd.DataFrame.from_dict(feed)
#    list_of_dfs.append(df)
#
#
#    #Table creation    
#    news = list_of_dfs[0]
#    news1 = list_of_dfs[0]
#    i = news1['title']
#
#    news1 = [item.replace("“","") for item in news1]
#    news1 = [item.replace("”",'') for item in news1]
#    news1 = [item.replace("’",'') for item in news1]
#    news1 = [item.replace("—",'--') for item in news1]
#    
#    
#    
#    news1 = i[0]
#    news2 = i[1]
#    news3 = i[2]
#    news4 = i[3]
#    
#    
#    link1 = news['link'][0]
#    link2 = news['link'][1]
#    link3 = news['link'][2]
#    link4 = news['link'][3]
#    return news1, news2, news3, news4, link1, link2, link3, link4
    

if __name__ == "__main__":

    
    html_text = requests.get(f'https://coinmarketcap.com/currencies/ethereum/').text
    soup = BeautifulSoup(html_text, 'lxml')

    
    
#check name_formatting 
    name = name_formatting('ethereum')

#check find_text
    rank = find_text('div', 'namePill namePillPrimary')

    pytrends = TrendReq()
    #Payload method 
    kw_list = [name] # list of keywords to get data 
    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')    

#check get_Google_interest
    interest = get_Google_interest()

#check get_top_Google_interest
    top_Regions = get_top_Google_interest()

#check get_related_queries
    top_related_queries = get_related_queries()

    gn = GoogleNews()

#Check get_titles 
    news = get_titles('ethereum')

    top_news = get_top_news('ethereum')




