"""
module 1: capstone introduction and understading the dataset
SpaceX Falcon 9 first stage Landing Prediction
Hands-on Lab: Complete the Data Collection API Lab
"""

import sys

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=[i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass=unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass=mass[0:mass.find("kg")+2]
    else:
        new_mass=0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    colunm_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name    
print("----TASK 1 -------")
"""
TASK 1: Request the Falcon9 Launch Wiki page from its URL
First, let's perform an HTTP GET method to request the Falcon9 Launch HTML page, as an HTTP response.
"""
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; data-science-script/1.0)"
}

response = requests.get(static_url, headers=headers)

print(response.status_code)
print(response.text[:500])  # preview the first 500 characters


"""
Create a BeautifulSoup object from the HTML response:
"""
soup = BeautifulSoup(response.text, "html.parser")

print(response.status_code)
print(response.headers.get("Content-Type"))
print(response.text[:200])

#Print the page title to verify if the BeautifulSoup object was created properly:
print(soup.title.string)


"""
TASK 2: Extract all column/variable names from the HTML table header
Next, we want to collect all relevant column names from the HTML table header
Let's try to find all tables on the wiki page first. If you need to refresh your memory about BeautifulSoup, please check the external reference link towards the end of this lab:

"""
print("------ TASK 2 -------")
html_tables = soup.find_all("table")
print(len(html_tables)) # should prompt 25
# Let's print the third table and check its content
first_launch_table = html_tables[2]
#print(first_launch_table)

"""
Next, we just need to iterate through the <th> elements and apply the provided extract_column_from_header() to extract column name one by one
"""
column_names = []

for th in first_launch_table.find_all("th"):
    name = extract_column_from_header(th)
    if name is not None and len(name) > 0:
        column_names.append(name)

print(f"-----COLUMN NAMES ---- \n {column_names}")

"""
TASK 3: Create a data frame by parsing the launch HTML tables
We will create an empty dictionary with keys from the extracted column names in the previous task. Later, this dictionary will be converted into a Pandas dataframe

"""
launch_dict= dict.fromkeys(column_names)

# Remove an irrelvant column
del launch_dict['Date and time ( )']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

"""
To simplify the parsing process, we have provided an incomplete code snippet below to help you to fill up the launch_dict. Please complete the following code snippet with TODOs or you can choose to write your own logic to parse all launch tables:
"""
launches_data = []  # list to hold all launch dictionaries
extracted_row = 0

for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    for rows in table.find_all("tr"):
        # Check if first table heading is a number corresponding to flight number
        if rows.th and rows.th.string:
            flight_number = rows.th.string.strip()
            flag = flight_number.isdigit()
        else:
            flag = False

        # Get table cells
        row = rows.find_all('td')

        # If it’s a valid flight number row, extract data
        if flag:
            extracted_row += 1
            datatimelist = date_time(row[0])  # returns [date, time]

            # check if customer doesn't exists:
            cell = row[6]
            a_tag = cell.find("a")
            customer = a_tag.string.strip() if a_tag and a_tag.string else None

            # Create dictionary for this launch
            launch_dict = {
                "Flight No.": flight_number,
                "Date": datatimelist[0].strip(','),
                "Time": datatimelist[1],
                "Version Booster": booster_version(row[1]) or row[1].a.string,
                "Launch Site": row[2].a.string,
                "Payload": row[3].a.string,
                "Payload mass": get_mass(row[4]),
                "Orbit": row[5].a.string,
                "Customer": customer,
                "Launch outcome": list(row[7].strings)[0],
                "Booster landing": landing_status(row[8])
            }

            # Append this dictionary to the list
            launches_data.append(launch_dict)

# Optional: see how many rows were extracted
print(f"Total launches extracted: {extracted_row}")
print(launches_data[:3])  # preview first 3 launches

"""
After you have fill in the parsed launch record values into launch_dict, you can create a dataframe from it.
"""
df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })
print(f"-----DATAFRAME ------\n{df}")

"""
We can now export it to a CSV for the next section, 
"""

"""
falcon 9 launches

"""
df.to_csv('spacex_web_scraped.csv', index=False)


# Get all launches
response = requests.get("https://api.spacexdata.com/v4/launches")
data = response.json()

# Normalize to dataframe
df = pd.json_normalize(data)

# Filter out Falcon 1 boosters
falcon9_df = df[df['rocket'].str.contains('Falcon 9', na=False)]

print(f" FALCON 9 LAUNCHES = {len(falcon9_df)}")



