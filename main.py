from bs4 import BeautifulSoup
import requests
import pandas as pd

#Base url for our results of interest, used for paging
base_url = 'https://erc.europa.eu/projects-figures/erc-funded-projects/results?items_per_page=100&f%5B0%5D=tid%253Aparents_all%3A60&f%5B1%5D=tid%253Aparents_all%3A72&f%5B2%5D=tid%253Aparents_all%3A73&f%5B3%5D=tid%253Aparents_all%3A74&f%5B4%5D=tid%253Aparents_all%3A75&f%5B5%5D=tid%253Aparents_all%3A76&f%5B6%5D=tid%253Aparents_all%3A77&f%5B7%5D=tid%253Aparents_all%3A78&f%5B8%5D=tid%253Aparents_all%3A79&f%5B9%5D=tid%253Aparents_all%3A80&f%5B10%5D=country%3ASweden&f%5B11%5D=country%3ADenmark&f%5B12%5D=country%3ANorway'
#HTML pointers, the page is messy
pointers = ['views-row views-row-1 views-row-odd views-row-first','views-row views-row-100 views-row-even views-row-last']

#Fabricate all pointers, url contains 100 results per page
for i in range(2,100):
    if (i % 2) == 0:
        pointer = 'views-row views-row-'+str(i)+ ' views-row-even'
        pointers.append(pointer)
    else:
        pointer = 'views-row views-row-' + str(i) + ' views-row-odd'
        pointers.append(pointer)
del pointer

#Information to extract
project_acron = []
project_name = []
PI = []
country = []
uni = []
Funding = []
description = []
start_date = []
end_date = []

#Iterate through pages
for page in range(0, 5):
    # Build the url for the page
    url=base_url+'&page='+str(page)
    #Extract HTML text and parse
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'html.parser')
    for pointer in pointers: #iterate through with the custom pointers
        project = soup.find('div', class_ = pointer) # project divisor, all info of that project is there
        if project is not None: #Failsafe
            acron = project.find('div', class_ = 'views-field views-field-acronym').find('span', class_ = 'field-content').text
            name = project.find('div', class_ = 'views-field views-field-title').find('span', class_ = 'field-content').text
            human = project.find('div', class_ = 'views-field views-field-xml-researcher').find('span', class_ = 'field-content').text
            host_country =  project.find('div', class_ = 'views-field views-field-country').find('span', class_ = 'field-content').text
            host_uni = project.find('div', class_ = 'views-field views-field-hostInstitution-name').find('span', class_ = 'field-content').text
            text = project.find('div', class_ = 'views-field views-field-nothing-2').find('span', class_ = 'field-content').find('div', class_ = 'collapse').text
            moneys=text.split('\n')[-5]
            dates= text.split('\n')[-2].split(' ')

            project_acron.append(acron)
            project_name.append(name)
            PI.append(human)
            country.append(host_country)
            uni.append(host_uni)
            description.append(text)
            Funding.append(moneys)
            start_date.append(dates[4].replace(',',''))
            end_date.append(dates[-1])
        else:
            pass

# Build the dataframe
df = pd.DataFrame(list(zip(project_acron, project_name, PI,country,uni, Funding, start_date, end_date, description)),
               columns =['Project_Acron', 'Project_name', 'PI','Country', 'University', 'Funding', 'Start_date','End_date','Description'])
#Write your results
df.to_excel('result.xlsx')
