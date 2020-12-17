#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
from datetime import date


# In[2]:


file_json_full = 'ftp://atviriduomenys.nvsc.lt/COVID19.json'
json_data_full = pd.read_json(file_json_full)


# In[3]:


json_data_full['Susirgimo data'] = pd.to_datetime(json_data_full['Susirgimo data']) #"Start of sickness" 
json_data_full['Atvejo patvirtinimo data'] = pd.to_datetime(json_data_full['Atvejo patvirtinimo data']) #"Positive test date"


# In[4]:


display(json_data_full.head(2))
display(json_data_full.info())


# In[5]:


"""
display(json_data_full['Įvežtinis'].value_counts())
display(json_data_full['Šalis'].value_counts())
display(json_data_full['Išeitis'].value_counts())
display(json_data_full['Užsienietis'].value_counts())
display(json_data_full['Atvejo amžius'].value_counts())
display(json_data_full['Lytis'].value_counts())
display(json_data_full['Savivaldybė'].value_counts())
display(json_data_full['Ar hospitalizuotas'].value_counts())
display(json_data_full['Gydomas intensyvioje terapijoje'].value_counts())
display(json_data_full['Turi lėtinių ligų'].value_counts())
"""


# In[6]:


#gender
json_data_full['Lytis'].replace('mot.','Moteris', inplace  = True)
json_data_full['Lytis'].replace('','nėra duomenų', inplace  = True)
display(json_data_full['Lytis'].value_counts())


# In[7]:


json_data_full['Išeitis'].replace('','nėra duomenų', inplace  = True)
json_data_full['Išeitis'].replace('Kita','nėra duomenų', inplace  = True)
display(json_data_full['Išeitis'].value_counts())


# In[8]:


json_data_full['Atvejo amžius'].replace('','nėra duomenų', inplace  = True)
display(json_data_full['Atvejo amžius'].value_counts())


# In[9]:


json_data_full['Gydomas intensyvioje terapijoje'].replace('','Ne', inplace  = True)
json_data_full['Turi lėtinių ligų'].replace('','Ne', inplace  = True)
display(json_data_full['Gydomas intensyvioje terapijoje'].value_counts())
display(json_data_full['Turi lėtinių ligų'].value_counts())


# In[10]:


display(json_data_full.head(2))
json_data_full = json_data_full[json_data_full['Išeitis'] != 'Nesirgo']


# In[11]:


covid_grouped = json_data_full.groupby(['Atvejo patvirtinimo data', 'Išeitis']).agg({'Išeitis':'count'}).rename(columns={'Išeitis':'Total_Number'}).reset_index()
covid_table = covid_grouped.pivot_table(index=['Atvejo patvirtinimo data'], 
                    columns='Išeitis', 
                    values='Total_Number',
                    fill_value=0).reset_index(drop=False)


covid_table = covid_table[['Atvejo patvirtinimo data','Gydomas', 'Pasveiko','Mirė', 'nėra duomenų']]
covid_table['Total per day'] = covid_table['Gydomas']+covid_table['Pasveiko']+covid_table['Mirė']+covid_table['nėra duomenų']
covid_table['Running: currently sick'] = covid_table['Gydomas'].cumsum(skipna = True)
covid_table['Running: recovered'] = covid_table['Pasveiko'].cumsum(skipna = True)
covid_table['Running: died'] = covid_table['Mirė'].cumsum(skipna = True)
covid_table['Running: unknown'] = covid_table['nėra duomenų'].cumsum(skipna = True)
covid_table['Running: Total'] = covid_table['Running: currently sick']+covid_table['Running: recovered']+covid_table['Running: died']+covid_table['Running: unknown']
covid_table['Running: Completed'] = covid_table['Running: recovered']+covid_table['Running: died']


display(covid_table.tail(10))


# In[12]:


import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(15,7),facecolor = "#F5F5F5")

ax.plot(covid_table['Atvejo patvirtinimo data'], covid_table['Running: Total'] , color = "red", label='Total cases')
ax.plot(covid_table['Atvejo patvirtinimo data'], covid_table['Running: Completed'], color = "blue", label = "Completed cases (recovery or death)")
ax.plot(covid_table['Atvejo patvirtinimo data'], covid_table['Running: died'], color = "Black", label='Total deaths')

ax.set_xlabel('Date', fontsize=18)
ax.set_ylabel('Cases',fontsize=18)
ax.set_title("Covid -19 confirmed and completed (death or recovery) cases in Lithuania " , fontsize=24, pad=20)

X = np.array(covid_table['Atvejo patvirtinimo data'])

Y1 = np.array(covid_table['Running: Total'])
Y2 = np.array(covid_table['Running: Completed'])
Y3 = np.array(covid_table['Running: died'])
ax.fill_between(X, Y1,Y2,color='grey',alpha=.15)
ax.fill_between(X, Y2,Y3,color='green',alpha=.15)
ax.fill_between(X, Y3,0,color='black',alpha=.15)

plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
ax.legend()
plt.show()


# In[17]:


import matplotlib.pyplot as plt
import numpy as np

covid_table09 = covid_table[covid_table['Atvejo patvirtinimo data']>='2020-09-01']
fig, ax = plt.subplots(figsize=(15,7),facecolor = "#F5F5F5")

ax.plot(covid_table09['Atvejo patvirtinimo data'], covid_table09["Gydomas"] , color = "blue", label='New cases per day')
ax.plot(covid_table09['Atvejo patvirtinimo data'], covid_table09['Pasveiko'], color = "green", label = "Recovered per day")
ax.plot(covid_table09['Atvejo patvirtinimo data'], covid_table09['Mirė'], color = "black", label='New deaths per day')

ax.set_xlabel('Date', fontsize=18)
ax.set_ylabel('Cases',fontsize=18)
ax.set_title("Daily Covid -19 cases in Lithuania since 2020-09-01 " , fontsize=24, pad=20)


plt.axvline(x = date(2020,12,14), color='red', linestyle='--', linewidth=0.5) #start of tightened quarantine
plt.axvline(x = date(2020,12,16), color='black', linestyle='--', linewidth=0.5) #start of tightened quarantine

ax.axvspan(date(2020,12,14), date(2020,12,16), alpha=0.15, color='grey')
ax.axvspan(date(2020,12,16), date(2020,12,21), alpha=0.15, color='red')
ax.legend()

plt.annotate(' 2 days period before \n the start of tightened quarantine'
             ,xy = (date(2020,12,14),3000)
             ,xytext = (date(2020,11,15),3200),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()


# In[14]:


mobility_csv_file = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv'
c_size = 5000

mobility_dataLT = None
for chunk in pd.read_csv(mobility_csv_file,chunksize=c_size, parse_dates=['date']):
    chunk_result =  chunk[chunk['country_region']=="Lithuania"]
    
    if mobility_dataLT is None:
        mobility_dataLT = chunk_result
    else:
        mobility_dataLT = mobility_dataLT.append(chunk_result)

print(mobility_dataLT.shape)


# In[15]:


mobility_data_melted = pd.melt(mobility_dataLT, id_vars = ['country_region', 'sub_region_1', 'date'], 
                              value_vars = ['retail_and_recreation_percent_change_from_baseline',
                                            'grocery_and_pharmacy_percent_change_from_baseline',
                                            'parks_percent_change_from_baseline',
                                            'transit_stations_percent_change_from_baseline',
                                            'workplaces_percent_change_from_baseline',
                                            'residential_percent_change_from_baseline'])
display(mobility_data_melted.tail())


# In[16]:


import seaborn as sns
fig, ax = plt.subplots(figsize=(15,7),facecolor = "#F5F5F5")

#Selected aggregated data of Lithuania
mobility_data_melted = mobility_data_melted[mobility_data_melted['sub_region_1'].isna()] 
#Selected aggregated data of Lithuania from '2020-09-01'
mobility_data_melted09 = mobility_data_melted[mobility_data_melted['date']>='2020-09-01']

sns.lineplot(x= 'date',y ='value', data = mobility_data_melted09, hue = 'variable' )
ax.axvspan(date(2020,12,14), date(2020,12,16), alpha=0.1, color='red')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




