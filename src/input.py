import csv       # Find more about it
import requests
from bs4 import BeautifulSoup

#TODO: Find a solution to classmethod and staticmethod

# Input: Ticker and Quote
def getquote():
    ticker = input("Enter ticker: ")
    company_name = input("Enter company name: ")
    return{'ticker': ticker,
           'company_name': company_name}

#Build up the URL for the index page
def company_list(new_ticker):
    firstpart = "http://economictimes.indiatimes.com/markets/stocks/"
    secondpart = "stock-quotes?ticker="
    secondpart = secondpart + new_ticker['ticker']
    listpage = firstpart + secondpart
    return listpage

# Calling getquote() and company_list()
new_ticker=getquote()
listpage=company_list(new_ticker)

# Parsing tho=rough the index page and collecting the HTML
index_request = requests.get(listpage)
index_content = index_request.content
index_soup = BeautifulSoup(index_content, 'html.parser')

# To find all the 'a tags' in the HTML
link =  index_soup.find_all('a')

# Fetching the tag with the desired stock
flag = 0
stockquote = ''
for sublink in link:
    if(new_ticker['company_name'] in sublink):
        flag = 1
        stockquote = str(sublink)

# Splitting the stock url to get the bit of URL with the company id
if(stockquote == ''):
    print('Check Company Name!')
else:
    stockquote = stockquote.split('"')
    stockname = stockquote[1]

# Joining the full URL to visit the Quote page
    halfstockurl = "http://economictimes.indiatimes.com"
    stockurl = halfstockurl+stockname

# Fetching the HTML from the stock page
    stock_request = requests.get(stockurl)
    stock_content = stock_request.content
    stock_soup = BeautifulSoup(stock_content,'html.parser')

# Stripping the Price tag to get the Price
    element = stock_soup.find('div',{'class': 'value'})
    price = element.text.strip()
    print(price)


