import csv       # Find more about it
import requests
from bs4 import BeautifulSoup

#TODO: Find a solution to classmethod and staticmethod
'''
# Input: Ticker and Quote
def getquote():
    ticker = input("Enter ticker: ")
    company_name = input("Enter company name: ")
    return{'ticker': ticker,
           'company_name': company_name}
'''
#Build up the URL for the index page
def getticker(n):
    firstpart = "http://economictimes.indiatimes.com/markets/stocks/"
    secondpart = "stock-quotes?ticker="
    secondpart = secondpart + n
    listpage = firstpart + secondpart
    return listpage


# Working with the CSV file
listofticker = []
listofquote = []
listofprice = []
with open("C:\\Users\\hp\\Documents\\PythonProjects\\b.csv",'r') as file:
    readcontent = csv.DictReader(file)
    for row in readcontent:
        for r in row:
            if(r == 'Ticker'):
                if(row[r] != ''):
                    listofticker.append(row[r])
            if(r == 'Name'):
                if(row[r] != ''):
                    listofquote.append(row[r])
            '''if(r == 'M.P'):
                if(row[r] != ''):
                    listofprice.append(row[r])'''


count = 0
while(count<len(listofticker)):
    listpage=getticker(listofticker[count])
#listpage=listofquote[count]

# Parsing through the index page and collecting the HTML
    index_request = requests.get(listpage)
    index_content = index_request.content
    index_soup = BeautifulSoup(index_content, 'html.parser')

    # To find all the 'a tags' in the HTML
    link =  index_soup.find_all('a')

    # Fetching the tag with the desired stock
    stockquote = ''
    for sublink in link:
        if(listofquote[count] in sublink):
                stockquote = str(sublink)

    # Splitting the stock url to get the bit of URL with the company id
    if(stockquote == ''):
        print('Check Company Name!')
    else:
        stockquote = stockquote.split('"')
        stockname = stockquote[1]

    # Joining the full URL to visit the Company page
        halfstockurl = "http://economictimes.indiatimes.com"
        stockurl = halfstockurl+stockname

    # Fetching the HTML from the stock page
        stock_request = requests.get(stockurl)
        stock_content = stock_request.content
        stock_soup = BeautifulSoup(stock_content,'html.parser')

    # Stripping the Price tag to get the Price
        element = stock_soup.find('div',{'class': 'value'})
        price = element.text.strip()
        listofprice.append(price)
        print(price)
        count+=1

print()

    # Again working with CSV File
count = 0
with open("C:\\Users\\hp\\Documents\\PythonProjects\\b1.csv",'w') as file:
    fieldnames = ['Company','M.P']
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    while count<len(listofticker):
        writer.writerow({'Company': listofquote[count], 'M.P': listofprice[count]})
        count+=1


pause_screen = input("Enter any key to exit")

#TODO: visit "http://stackoverflow.com/questions/1007481/how-do-i-replace-whitespaces-with-underscore-and-vice-versa" to find more methods to urlify

'''
def urlify(s):
# Remove all non-word characters (everything except numbers and letters)
s = re.sub(r"[^\w\s]", '', s)

# Replace all runs of whitespace with a single dash
s = re.sub(r"\s+", '-', s)
return s
'''

