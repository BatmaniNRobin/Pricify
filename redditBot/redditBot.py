#!/usr/bin/python
import praw
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("buildapcsales")
rowCount=2
columnCount=1
part=""
item=""
price=""

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Pricify-1d8fb47c5602.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Pricify Spreadsheet").sheet1

# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

for submission in subreddit.new(limit=15):
	try:
		part=submission.title[1:submission.title.index("]")]
		item=submission.title[submission.title.index("]")+1:submission.title.index("$")-1]
		price=submission.title[submission.title.index("$"):]
	except:
		print("Error")
	else:
		sheet.update_cell(rowCount,columnCount,part)
		sheet.update_cell(rowCount,columnCount+1,item)
		sheet.update_cell(rowCount,columnCount+2,price)
		sheet.update_cell(rowCount,columnCount+3,submission.url)
		rowCount+=1
	columnCount=1
	print("Part: ", part)
	print("Item: ", item)
	print("Price: ", price)
	print("---------------------------------\n")	
	
