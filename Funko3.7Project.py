from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


#set up the driver to start up server to get page source
options = webdriver.ChromeOptions();
options.add_argument('headless');
driver = webdriver.Chrome(options=options)


#greet and get input from the user
print("Hello and welcome to the funko pop pricing guide")
print("Please enter the name of the character you are looking for")
p = input()
funkoWebsite = 'https://www.hobbydb.com/marketplaces/poppriceguide/catalog_items?q='

products=[]
prices=[]

# we are assuming at this point that the raw_input is fine in every way with
# no spaces that would mess up this url
queryFunko = funkoWebsite + p

#testing the query is good
    
driver.get(queryFunko)
#waiting for enough time for page to give response if lots of items
time.sleep(4)
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

#parsing through returned html to find the name of the item and the price
for a in soup.findAll('div', attrs={'class':'catalog-item-card ng-scope'}):
    name=a.find('a', attrs={'class':'catalog-item-name ng-binding'})
    price=a.find('div', attrs={'class':'price-guide ng-scope ng-binding'})
    
    if name is None:
        prices.append(price.text[34: 44])
        products.append(name.text[15:len(name.text)-1])
df = pd.DataFrame({'Product Name':products,'Price':prices})
print(df.to_string())
