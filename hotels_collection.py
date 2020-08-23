#Libraries
from requests import get 
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 
import time 
import re 

#Html info to be used
url = 'https://www.hostelworld.com/hostels/Paris'
response = get(url)

#create the soup
soup = BeautifulSoup(response.text, 'html.parser')

#Individual container for each hostel
hostel= soup.find_all(class_ = 'fabresult rounded clearfix hwta-property')

#Get the number of pages
pages= soup.find_all(class_= 'pagination-page-number')
last_page = pd.to_numeric(pages[-1].text)
print(last_page) #5

#How many hostels we have on the first page
print(len(hostel))  #30

first_hostel = hostel[0]
print(first_hostel.prettify())


# Info to extract
    #Name 
    #Distance from center
    #Link
    #Rating
    #Number of reviews
    #Price in Euro
    

#Name
name = first_hostel.h2.a.text

#Distance
distance = float(first_hostel.find(class_ = 'addressline').text.strip().split(' ')[0].replace('km',''))

#Link
link = first_hostel.h2.a.get('href')

#Rating
rating = float(first_hostel.find(class_ = 'hwta-rating-score').text.strip())

#Num reviews
reviews = int(first_hostel.find(class_ = 'hwta-rating-counter').text.strip())

#price
price= float(first_hostel.find(class_ = 'price').text.replace('€', ''))





# FOR LOOPS 
noms = []
distance_km = []
liens = []
notes= []
avis = []
prix = []

for page in np.arange(1, last_page+1):
    url = 'https://www.hostelworld.com/hostels/Paris?page=' + str(page)
    response = get(url)
    soup= BeautifulSoup(response.text, 'html.parser')
    containers = soup.find_all(class_ = 'fabresult rounded clearfix hwta-property')
    
    for elem in range(len(containers)):
        noms.append(containers[elem].h2.a.text)
        distance_km.append(containers[elem].find(class_ = 'addressline').text.strip().split(' ')[0].replace('km',''))
        liens.append(containers[elem].h2.a.get('href'))
        notes.append(containers[elem].find(class_ = 'hwta-rating-score').text.strip())
        avis.append(containers[elem].find(class_ = 'hwta-rating-counter').text.strip())
        prix.append(containers[elem].find(class_ = 'price').text.replace('€', ''))
        
    time.sleep(3)
    
#Create DF

df = pd.DataFrame({'nom_hotel': noms, 'distance_centre_km': distance_km, 'note':notes,
                   'nb_avis':avis, 'prix':prix, 'lien':liens})

df.columns

num_cols = ['distance_centre_km', 'note', 'nb_avis', 'prix']
for col in num_cols:
    df[col]= pd.to_numeric(df[col], errors='coerce')
    
df.to_csv('hotelparis.csv', index=False)

df['note'].value_counts()