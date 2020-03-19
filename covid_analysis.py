# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:48:36 2020

@author: websterkgd
"""

#clear environment
from IPython import get_ipython;   
get_ipython().magic('reset -sf')
from IPython import get_ipython; 

#import packages for data analysis 
import pandas as pd
import os 

#change directory to directory with data
os.chdir('D:\\a_Desktops_Git\\Current\\SpringBoard\\Capstone')

#import the data
covid_data = pd.read_excel('COVID-19-geographic-disbtribution-worldwide-2020-03-17.xlsx')

#create a list of countries and drop duplicates
lc = covid_data['Countries and territories'].values
lc = [i for n, i in enumerate(lc) if i not in lc[n + 1:]]    

#create a dictionary of data frames
dc = {}
for i in lc:
    dc[i] = covid_data[covid_data['Countries and territories'] == i]
    dc[i].index = list(range(0,len(dc[i])))
    
# add a total cases column to each dataframe 
for key in dc:
    for i in dc[key]:
        dc[key]['tot_cases'] = list(range(0,len(dc[key]['Cases'])))
        for i in range(0,len(dc[key])):
            dc[key]['tot_cases'][i] = sum(dc[key]['Cases'][i:len(dc[key]['Cases'])])
            
print(dc['Afghanistan']['tot_cases'],dc['United_States_of_America']['tot_cases'])

#exploratory plotting
import matplotlib.pyplot as plt
import numpy as np 

dc['United_States_of_America']['tot_cases'].plot(marker='.', linewidth =0)
plt.show()

#fit regression models to each case
# limit countries to those with more than 100 cases
dcoh = {}
for key in dc.keys():
    if dc[key]['tot_cases'][0] >= 100:
        dcoh[key] = dc[key]    

#remove instances below fifty cases in the countries
for key in dcoh.keys():
    dcoh[key] = dcoh[key][dcoh[key]['tot_cases'] > 50]

#remove instances with less than four data points
dcohr = {}    
for key in dcoh.keys():
    if len(dcoh[key]['tot_cases']) > 3:
        dcohr[key] = dcoh[key]
        
#create column with increasing date
for key in dcohr.keys():
    dcohr[key]['AD50'] = list(range(0,len(dcohr[key]['Cases'])))[::-1]

#calculate the growth rate for each country 
grc = {}
for key in dcohr.keys():
    grc[key] = np.polyfit(dcohr[key]['AD50'], 
       np.log(dcohr[key]['tot_cases']), 1, 
       w=np.sqrt(dcohr[key]['tot_cases']))[0]

grc = pd.DataFrame.from_dict(grc, orient='index')

#quick histogram
import seaborn as sns
plt.boxplot(grc[0])
plt.show()

#swarmplot
sns.swarmplot(grc[0])
plt.show()

#find average air temperatures for countries in grc in Feb (C)
aat = {'Australia': 28, 'Austria':9.56,'Bahrain': 18.06,'Belgium':3.65, 
       'Brazil': 27, 'Canada': -2.5, 'China':-0.5, 'Czech_Republic': 1,
       'Denmark': 0.45, 'Egypt': 15.56, 'Estonia':-3.8,'Finland':1.8,
       'France': 8.6, 'Germany': 5.3, 'Greece':12.7, 'Iceland':0.4, 
       'India':18.2,'Indonesia':26.2, 'Iran': 6.2, 'Iraq': 13.1,'Ireland': 4.2, 
       'Israel':8.8, 'Italy':10.7, 'Japan':9, 'Kuwait':16.7, 'Lebanon':14.3,
       'Malaysia':29.4, 'Netherlands':6.9, 'Norway':-0.4, 'Philippines':27.8, 
       'Poland':3.6, 'Portugal':14.3, 'Qatar':20.2,'Romania':4.7,
       'San_Marino':8.7, 'Saudi_Arabia':19.1, 'Singapore':27.5,'Slovenia':4.5, 
       'South_Korea':3, 'Spain':11.5,'Sweden':1.3, 'Switzerland':5.7, 
       'Thailand':27.7, 'United_Kingdom':6.4, 'United_States_of_America':2.3}

#convert aat to dataframe
aat = pd.DataFrame.from_dict(aat, orient='index')

#merge aat and grc 
#first unindex these data frames 
aat = aat.reset_index()
grc = grc.reset_index()

#merge on index
aat_grc = pd.merge(left=aat, right=grc, left_on='index', right_on='index')

#rename columns
aat_grc.columns = ['country','ATF','GR']

#plot to examine relationship between growth rate and temp
plt.plot(aat_grc['ATF'], aat_grc['GR'], marker='.', linewidth=0)
plt.show()

#no obivous relationship between growth rate and temperature
#certainly not a strong relationship 
