import urllib.request as ur
from urllib.error import HTTPError
from bs4 import BeautifulSoup
#import sys

"""
url='http://www.pythonscraping.com/pages/page3.html'

#soup = BeautifulSoup(html)
html = urlopen(url)
soup = BeautifulSoup(open(html))
print(soup.prettify())
"""

"""
def getTitle(url):
    try:
        html = ur.urlopen(url)
    except HTTPError as e:
        print(e)
        print(e.reason)
        return None
    try:
        bsObj = BeautifulSoup(html,"html.parser")
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title


url='https://goo.gl/n5zK42'

resp = ur.urlopen(url)

title = getTitle(url)
if title == None:
    print("Title could not be found!")
elif 'AG322QCX' in str(title):
    print(title)
else:
    print("the appointed title not found")
"""

print("FROM MOMO:\n")

html = ur.urlopen("https://goo.gl/n5zK42")
bsObj = BeautifulSoup(html, "html.parser")
des = bsObj.find(attrs={"name":"Description"})
price = bsObj.find('span', 'prdPrice')
if 'AG322QCX' in str(des):
    print(des)
    print(price)
else:
    print("at MOMO could not found AG322QCX")



print("\n\n FROM YAHOO:\n")

html = ur.urlopen("https://goo.gl/mR7M6n")
bsObj = BeautifulSoup(html, "html.parser")
des = bsObj.find(attrs={"name":"description"})
price = bsObj.find('span', 'price')
if 'AG322QCX' in str(des):
    print(des)
    print(price)
else:
    print("at YAHOO could not found AG322QCX")


print("\n\n FROM UDN:\n")

html = ur.urlopen("https://goo.gl/Pn9QrM")
bsObj = BeautifulSoup(html, "html.parser")
des = bsObj.find(attrs={"name":"Keywords"})
price = bsObj.find('span', 'hlight')
if 'AG322QCX' in str(des):
    print(des)
    print(price)
else:
    print("at UDN could not found AG322QCX")
