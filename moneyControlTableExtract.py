# from pywinauto import Application
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def check_url(url):
    if (url.startswith('http')==False):
        url='https://'+url
        print(url)
    return url


# app = Application(backend='uia')
# app.connect(title_re=".*Chrome.*")
# dlg = app.top_window()
# url = dlg.child_window(title="Address and search bar", control_type="Edit").get_value()
# # print(url)
# url= check_url(url)
# print('URL extraction complete\n')






def bottom_table(soup):
    table_new = soup.find('table', attrs={"class": "peer_tbl"}) 
    
    
    #Extracting Headings
    
    body = table_new.find_all("tr")
    # Head values (Column names) are the first items of the body list
    head = body[0] # 0th item is the header row
    body_rows = body[1:] # All other items becomes the rest of the rows

    # Lets now iterate through the head HTML code and make list of clean headings

    # Declare empty list to keep Columns names
    headings = []
    for item in head.find_all("th"): # loop through all th elements
        # convert the th elements to text and strip "\n"
        item = (item.text).rstrip("\n")
        # append the clean column name to headings
        headings.append(item)

        
    #Extracting Data Values
    
    all_rows = [] # will be a list for list for all rows
    for row_num in range(len(body_rows)): # A row at a time
        row = [] # this will old entries for one row
        for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
            # row_item.text removes the tags from the entries
            # the following regex is to remove \xa0 and \n and comma from row_item.text
            # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
            aa = re.sub("(\xa0)|(\n)|(\t)|,","",row_item.text)
            #append aa to row - note one row entry is being appended
            row.append(aa)
        # append one row to all_rows
        all_rows.append(row)
    
    #Creating a Dataframe
    # We can now use the data on all_rowsa and headings to make a table
    # all_rows becomes our data and headings the column names
    df = pd.DataFrame(data=all_rows,columns=headings)
    df.to_csv('Money_Control_Extracted_table.csv')
    print(df)
    return df



def top_tables(soup):
    tables = soup.findAll('table') 
    
    selected_tables=tables[3:7]
    for table in selected_tables:
        table_rows=table.find('tbody').find_all('tr')

        headings=[]
        values=[]

        for row in table_rows:
            headings.append(row.find_all('td')[0].text)
            values.append(row.find_all('td')[1].text)


        df = pd.DataFrame(values,columns=['values'])
        df.index = headings
        print(df)
        print()








# Site URL
url="https://www.moneycontrol.com/india\
/stockpricequote/refineries/relianceindustries/RI"


# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse HTML code for the entire site
soup = BeautifulSoup(html_content, "lxml")

print("\n\n######### PRINTING TOP TABLES ###################\n ")
top_tables(soup)

print("\n\n######### PRINTING BOTTOM TABLE ###################\n ")
bottom_table(soup)


