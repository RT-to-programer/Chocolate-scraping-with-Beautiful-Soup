from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

res = requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html')

soup = BeautifulSoup(res.content, 'html.parser')

def scrape_column(class_name):
    column = []
    for i in soup.select('.'+class_name):
        column.append(i.get_text())
    return(column[1:])

headers = soup.find_all('tr')[2]
class_list = [value for i in headers('td') for value in i['class']]

#preparing data for dataframe
d = {}
for i in class_list:
    d[i] = scrape_column(i)
    
#make dataframe and clean data
df = pd.DataFrame.from_dict(d)
for i in df[['REF', 'ReviewDate', 'Rating']].columns:
    df[i] = pd.to_numeric(df[i])
    
df.CocoaPercent = pd.to_numeric(df.CocoaPercent.str.strip('%'))
df['CocoaPercentage'] = df.CocoaPercent
tidied_df = df[['Company', 'Origin', 'REF', 'ReviewDate', 'CocoaPercentage', 'CompanyLocation', 'Rating', 'BeanType', 'BroadBeanOrigin']]
    

#make histogram of rating
#ratings = pd.to_numeric(df['Rating'])
plt.hist(tidied_df.Rating)
plt.show()

#find top 10 companies and their avg rating
top10 = tidied_df.groupby('Company').mean().Rating.nlargest(10)
print(top10)

#Relationship between Cacao percent and rating (Scatterplot)
cocoapercentage_rating = tidied_df.groupby('Company').mean()[['CocoaPercentage', 'Rating']].nlargest(10, columns= 'CocoaPercentage')
print(cocoapercentage_rating)
plt.scatter(tidied_df.Rating, tidied_df.CocoaPercentage)
z = np.polyfit(tidied_df.CocoaPercentage, tidied_df.Rating, 1)
line_function = np.poly1d(z)
plt.plot(tidied_df.CocoaPercentage, line_function(tidied_df.CocoaPercentage), "r--")
plt.show()
plt.clf()

#Where are the best cocoa beans grown
best_beans_origin = tidied_df.groupby('BroadBeanOrigin').mean().Rating.nlargest(10)
print(best_beans_origin)

#Which countries produce the highest-rated bars
best_countries = tidied_df.groupby('CompanyLocation').mean().Rating.nlargest(10)
print(best_countries)