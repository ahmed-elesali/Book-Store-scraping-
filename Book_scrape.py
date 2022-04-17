import requests 
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os 


# url for data to scrape 
url = 'https://books.toscrape.com/'

#extract the content from the url
response = requests.get(url)
content = response.text

# get the soup data 
soup = BeautifulSoup(content , 'html.parser')

# creating file and open it to save data in it 
with open('Book.html','w') as file :
    file.write(content)

# function to get titles 

def book_title(soup):
    titles = soup.find_all('h3')
    book_title = []
    for tag in titles:
        b_title = tag.text.replace('...','')
        book_title.append(b_title)
    return(book_title)



# tracking the function output
print(book_title(soup))

print('CONTUINE','------'*10)
# function to get the price of the book 
def book_price(soup):
    Book_price_tags = soup.find_all('p', class_ = 'price_color')
    Book_price = []
    for tags in Book_price_tags:
        price = tags.text.replace('Â','')
        Book_price.append(price.replace('£',''))
    return Book_price


print(book_price(soup))
print('CONTUINE','------'*10)
# get the stock avilabilty
def stock_avilabilty(soup):
    book_tag = soup.find_all('p', class_ ="instock availability")
    book_list = []
    for tags in book_tag:
        book_list.append(tags.text.strip())
    return(book_list)


# tracking the function output
print(stock_avilabilty(soup))
print('CONTUINE','------'*10)

# get the url fro every link in the code 
titles = soup.find_all('h3')
def get_book_url(titles):
    Book_url = []
    for article in titles:
        for link in article.find_all('a', href = True):
            url = link['href']
            links = 'https://books.toscrape.com/' + url
            if links not in Book_url:
                Book_url.append(links)
    return Book_url

# tracking the function output
print(get_book_url(titles))
print('CONTUINE','------'*10)
# load multible page
def get_doc(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(response))
    return soup

# loop throw every page 
def scrape_multiple_pages(n):
    url = 'https://books.toscrape.com/catalogue/page-'
    titles,prices,stocks_availability,urls = [],[],[],[]
    
    for page in range(1,n+1):
        soup = get_doc(url + str(page)+ '.html')
        titles.extend(book_title(soup))
        prices.extend(book_price(soup))
        stocks_availability.extend(stock_avilabilty(soup))
        urls.extend(get_book_url(soup.find_all('h3')))
        
    book_dict1 = {
                'TITLE':titles,
                'PRICE':prices,
                'STOCK AVAILABILTY':stocks_availability,
                'URL':urls}
    return pd.DataFrame(book_dict1)

# save the data into csv file 
scrape_multiple_pages(50).to_csv('scrap_book.csv',index = None)
print('finshed','-_-')