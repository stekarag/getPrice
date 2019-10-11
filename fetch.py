import requests
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import html5lib
import re
import time
import random
import sys

def getPrice(url):
	print("Retrieving ",url)
	try:
		session = requests.Session()
		req = session.get(url)
	except HTTPError:
		print("HTTP ERROR")
		return None
	except TimeoutError:
		print("Connection timed  out")
		return None
	try:
		pgObj = BeautifulSoup(req.text, "html5lib") #	
		q = pgObj.find_all(attrs={'class': 'price'})
	except AttributeError:
		print("Attribute Error")
		return None
	print("%d item(s) found"%len(q))
	try:
		qtag = str(q[0])
		pattern = r'\d{1,2},\d{2}'
		price = re.search(pattern, qtag).group(0)
	except IndexError:
		print("String manipulation error")
		return None
	return price

pattern = r'\d{13}'
try:
	arg1 = sys.argv[1]
except IndexError:
	print("No argument given. Exiting...")
	exit()
try:
	match = re.match(pattern, arg1).group(0)
	barcode = match
except AttributeError:
	barcode = None	
	if barcode == None:
		print("No barcode found")
else:
	print("Barcode requested is ",barcode)
uri = "https://www.caremarket.gr/apotelesmata-anazitisis/?Query=%s"%barcode
#print("URI is ",uri)
price = getPrice(uri)
if price == None:
	print("Price could not be found")
else:
	print("Price is ",price)
