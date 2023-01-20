#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 11:06:43 2023

@author: goudurix
"""

import os 
path = "/Users/goudurix/Desktop/tutos_Data/Data_Scrapper/"
os.chdir(path)

from function import * 
import pandas as pd 
from pytrends.request import TrendReq
import numpy as np 
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from IPython.display import set_matplotlib_formats
import matplotlib.pyplot as plt
from pygooglenews import GoogleNews
from fpdf import FPDF
import matplotlib as mpl
from matplotlib.ticker import ScalarFormatter

#==============================================================================
#functions
#==============================================================================

def find_text(tag, var):
    text = soup.find(tag, class_ = var).text
    return text

def get_Google_interest():
    interest = pytrends.interest_over_time()
    return interest

def get_top_Google_interest(): 
    regions = pytrends.interest_by_region(resolution= 'COUNTRY', inc_low_vol=True, inc_geo_code=False) 
    regions.sort_values(by=[name], inplace=True, ascending=False)
    regions.head(10)
    regions= list(regions.index)
    region1= regions[0]
    region2= regions[1]
    region3= regions[2]
    region4= regions[3]
    region5= regions[4]
    region6= regions[5]
    region7= regions[6]
    region8= regions[7]
    region9= regions[8]
    region10= regions[9]   
    return region1, region2, region3, region4, region5, region6, region7, region8, region9, region10

def get_related_queries():
    queries = pytrends.related_queries()
    queries= queries[name]['top'][:10]
    querie1= queries['query'][0]
    querie2= queries['query'][1]
    querie3= queries['query'][2]
    querie4= queries['query'][3]
    querie5= queries['query'][4]   
    return querie1, querie2, querie3, querie4, querie5

def get_titles(search): 
    stories = []
    search = gn.search(search, when ='6d')
    newsitem = search['entries']
    for item in newsitem:
        story = {
            'title': item.title,
            'link' : item.link
        }
        stories.append(story)
    return stories[:20]

def get_top_news(name):
    list_of_dfs= list()
    keyword = name + " news"

    #Data Gathering
    feed = get_titles(keyword)
    df = pd.DataFrame.from_dict(feed)
    list_of_dfs.append(df)


    #Table creation    
    news = list_of_dfs[0]
    news1 = list_of_dfs[0]
    i = news1['title']

    news1 = [item.replace("“","") for item in news1]
    news1 = [item.replace("”",'') for item in news1]
    news1 = [item.replace("’",'') for item in news1]
    news1 = [item.replace("—",'--') for item in news1] 
    
    news1 = i[0]
    news2 = i[1]
    news3 = i[2]
    news4 = i[3]
    
    link1 = news['link'][0]
    link2 = news['link'][1]
    link3 = news['link'][2]
    link4 = news['link'][3]
    return news1, news2, news3, news4, link1, link2, link3, link4

#==============================================================================
#Data Scrapping part 
#==============================================================================
    
name = input("Enter the name of the project you want to research: ")

name = name_formatting(name)

#get html text from CoinmarketCap
html_text = requests.get(f'https://coinmarketcap.com/currencies/{name}/').text
soup = BeautifulSoup(html_text, 'lxml')

#Create Title variable
Title = name + " overview report"

#Get project rank
Rank = find_text('div', 'namePill namePillPrimary')

#Get cryptocurrency price 
price = find_text('div', 'priceValue')

#Get High and Low price 
priceSlider = soup.find('div', class_ = 'sc-aef7b723-0 kIYhSM')
Low = priceSlider.find('span', class_ = 'sc-fe06e004-5 jXIGCe').text

priceSlider = soup.find('div', class_ = 'sc-aef7b723-0 gjeJMv')
High = priceSlider.find('span', class_ = 'sc-fe06e004-5 jXIGCe').text

#Get resources links
resource_block = soup.find('div', class_ = 'sc-aef7b723-0 sc-b83c9ecb-3 edVIPP')
resource_link = resource_block.find_all('a', class_ = 'link-button')

link = []
for l in resource_link :
    link.append(l.get_attribute_list('href'))
len1 = len(link)


#Get market metrics
#MarketCap, DilutedMarketCap, Volume24, Circulating Supply
metrics = soup.find_all('div', class_ = 'statsValue')
MarketCap= metrics[0].text
DilutedMarketCap = metrics[1].text
Volume24 = metrics[2].text
CirculatingSupply = metrics[3].text

#Pricevalue, DEX Volume, MaxSupply
metrics = soup.find_all('div', class_ = 'sc-aef7b723-0 iDBUa-D')
PriceValue = metrics[0].find('div', class_ = 'priceValue').text
DEXvol = metrics[1].find('div', class_ = 'volValue').text
MaxSupply = metrics[2].find('div', class_ = 'maxSupplyValue').text

#Total supply, CEX Volume 
metrics = soup.find_all('div', class_ = "sc-aef7b723-0 hXeEQW")
CEXvol = metrics[0].find('div', class_ = 'volValue').text
TotalSupply1 = metrics[1].find('div', class_ = 'maxSupplyValue').text

#Get Project Overview analysis 

overview = soup.find('div', class_ = 'sc-7fc09d63-0 hkVaBd')
paragraphs = overview.find_all('p')
analysis = []
counter = 0
for t in paragraphs: 
    analysis.append(paragraphs[counter].text)
    counter = counter + 1
    
#==============================================================================
#Google Trend part 
#==============================================================================

pytrends = TrendReq()

#Payload method 
kw_list = [name] # list of keywords to get data 
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')


#Google Interests
google_interest = get_Google_interest()

#Create google interest graph
set_matplotlib_formats('retina', quality=100)


# Set default figure parameters.
plt.rcParams['figure.figsize'] = (8, 5)

fig, ax = plt.subplots()

ax.bar(
    x=google_interest.index,
    height=google_interest[name], 
    width= 0.8
)

date_form = DateFormatter("%b")
ax.xaxis.set_major_formatter(date_form)

# removal of the top, right and left spines (figure borders)
# make the bottom spine gray instead of black.
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')

# removal of the ticks
ax.tick_params(bottom=False, left=False)

# Add a horizontal grid (but keep the vertical grid hidden).
# Color the lines in light gray.
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)        
         
fig.tight_layout()
fig.savefig('/Users/goudurix/Desktop/tutos_Data/Data_scrapper/GoogleInterest.png')


#Get interest by region 
regions_interest = get_top_Google_interest()
region1= regions_interest[0]
region2= regions_interest[1]
region3= regions_interest[2]
region4= regions_interest[3]
region5= regions_interest[4]
region6= regions_interest[5]
region7= regions_interest[6]
region8= regions_interest[7]
region9= regions_interest[8]
region10= regions_interest[9]

#Get related queries
queries = get_related_queries()
querie1= queries[0]
querie2= queries[1]
querie3= queries[2]
querie4= queries[3]
querie5= queries[4]

#==============================================================================
#Google News Part 
#==============================================================================

gn = GoogleNews()
latest_new = get_top_news('ethereum')
news1 = latest_new[0]
news2 = latest_new[1]
news3 = latest_new[2]
news4 = latest_new[3]
link1 = latest_new[4]
link2 = latest_new[5]
link3 = latest_new[6]
link4 = latest_new[7]


#==============================================================================
#PDF Generation Part
#==============================================================================


#Margin
m = 10 
# Page width : Width of A4 is 210mm 
pw = 210 - 2*m 
# Cell height 
ch = 50

pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.add_page()
pdf.set_text_color( 255, 255, 255)
pdf.image('/Users/goudurix/Desktop/tutos_Data/Data_Scrapper/Diapositive1.jpeg', 0, 0, 210, 303)

#Title 
pdf.set_font('Helvetica', '', 34)
pdf.set_xy(x=8, y = 11)
pdf.cell(w=200, h=20, txt= Title, border=0, ln=0, align ='L')

pdf.set_font('Helvetica', '', 12.5)

#1st Row
pdf.set_xy(x=14, y = 35)
pdf.cell(w=53, h=10, txt= name, border=0, ln=0, align ='C')

pdf.set_xy(x=79, y = 35)
pdf.cell(w=53, h=10, txt= Volume24, border=0, ln=0, align ='C')

pdf.set_xy(x=143, y = 35)
pdf.cell(w=53, h=10, txt= TotalSupply1, border=0, ln=0, align ='C')


#2nd Row
pdf.set_xy(x=14, y = 55)
pdf.cell(w=53, h=10, txt= Rank, border=0, ln=0, align ='C')

pdf.set_xy(x=79, y = 55)
pdf.cell(w=53, h=10, txt= MarketCap, border=0, ln=0, align ='C')

pdf.set_xy(x=143, y = 55)
pdf.cell(w=53, h=10, txt= price, border=0, ln=0, align ='C')


#3nd Row
pdf.set_xy(x=14, y = 85.5)
pdf.cell(w=53, h=10, txt= CirculatingSupply, border=0, ln=0, align ='C')

pdf.set_xy(x=79, y = 85.5)
pdf.cell(w=53, h=10, txt= DilutedMarketCap, border=0, ln=0, align ='C')

pdf.set_xy(x=143, y = 85.5)
pdf.cell(w=53, h=10, txt= High, border=0, ln=0, align ='C')


#4th Row
pdf.set_xy(x=14, y = 105)
pdf.cell(w=53, h=10, txt= DEXvol, border=0, ln=0, align ='C')

pdf.set_xy(x=79, y = 105)
pdf.cell(w=53, h=10, txt= CEXvol, border=0, ln=0, align ='C')

pdf.set_xy(x=143, y = 105)
pdf.cell(w=53, h=10, txt= Low, border=0, ln=0, align ='C')

pdf.image('/Users/goudurix/Desktop/tutos_Data/Data_Scrapper/GoogleInterest.png', x = 20, y = 142.2, w = 170, h = 63)


#Regional Interest
pdf.set_font('Helvetica', '', 11)
pdf.set_xy(x=11, y = 224.3)
pdf.cell(w=40, h=5, txt= region1 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 229.3)
pdf.cell(w=40, h=5, txt= region2 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 234.3)
pdf.cell(w=40, h=5, txt= region3 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 239.6)
pdf.cell(w=40, h=5, txt= region4 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 245)
pdf.cell(w=40, h=5, txt= region5 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 250)
pdf.cell(w=40, h=5, txt= region6 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 255)
pdf.cell(w=40, h=5, txt= region7 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 260)
pdf.cell(w=40, h=5, txt= region8 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 265.3)
pdf.cell(w=40, h=5, txt= region9 , border=0, ln=0, align ='L')

pdf.set_xy(x=11, y = 270.5)
pdf.cell(w=40, h=5, txt= region10 , border=0, ln=0, align ='L')


#News
pdf.set_font('Helvetica', '', 10)
pdf.set_xy(x=88, y = 230)
pdf.multi_cell(w=110, h=5, txt= news1, border =0, 
                align = 'L')
pdf.link(x=88, y=230, w=110, h=5, link= link1 )


pdf.set_xy(x=88, y = 246)
pdf.multi_cell(w=110, h=5, txt= news2, border = 0, 
                align = 'L')
pdf.link(x=88, y=246, w=110, h=5, link= link2 )

pdf.set_xy(x=88, y = 262)
pdf.multi_cell(w=110, h=5, txt= news3, border = 0, 
                align = 'L')
pdf.link(x=88, y=262, w=110, h=5, link= link3 )


#2nd page
pdf.add_page()
pdf.image('/Users/goudurix/Desktop/tutos_Data/Data_Scrapper/Diapositive2.jpeg', 0, 0, 210, 303)

pdf.set_font('Helvetica', '', 12)

#Resources links 
pdf.set_xy(x=10, y = 22.5)
for s in range(len1 -1):
    x = link[s][0] + "\n"
    pdf.write(5, x)


#Project Overview 
pdf.set_font('Helvetica', '', 12)
space = 0
new_list = analysis
new_list = [item.replace("“","") for item in new_list]
new_list = [item.replace("”",'') for item in new_list]
new_list = [item.replace("’",'') for item in new_list]
new_list = [item.replace("—",'--') for item in new_list]



pdf.set_xy(x=10, y = 100)
for s in range(8):
    x = new_list[s] + "\n"
    pdf.write(5, x)

pdf.output(f'./Report.pdf', 'F')








