# Tool to identify leasehold/freehold info from the UK land registry site
# Set the variables below, output is a csv file containing the list of properties and the tenant/leasehold status
# Tool uses selenium on Firefox via geckodriver on Windows

import time
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# Set variables

# eservice credntials
username = 'XXX' # Username for Land Registry eservice account
pwd = 'XXX' # Password for Land Registry eservice account

waitTime = 5 # Crudely wait for page to load (time in seconds)
query = 'Leasehold' # Search for this string on the page. If it exists, then it's a leasehold property

# Properties to be searched on the eservices site via the "detailed enquiry" link
flats = range(1,246) # Flat numbers of interest
street = 'XXX' # Street Name
town = 'XXX' # Town

# Define functions

#Log in to eservices using the supplied credentials and go to the Detailed Enquiry page
def loginEservices(username, pwd):
    userElem = browser.find_element_by_id('username')
    userElem.send_keys(username)
    passwordElem = browser.find_element_by_id('password')
    passwordElem.send_keys(pwd)
    passwordElem.submit()
    time.sleep(waitTime)
    linkElem = browser.find_element_by_link_text('Detailed enquiry')
    linkElem.click() # follow the "Detailed enquiry" link to search by flat number
    time.sleep(waitTime)

# Fill in the search form with the address variables and run the query
def searchSite(flats,street,town):
    flatNo = browser.find_element_by_id('flatNo')
    flatNo.send_keys(flats)
    streetName = browser.find_element_by_id('streetName')
    streetName.send_keys(street)
    townName = browser.find_element_by_id('townName')
    townName.send_keys(town)
    townName.submit()
    time.sleep(waitTime)

# Search for the query term, if it exists then it's a leasehold property
def leaseholdSearch(query):
    if (query in browser.page_source):
        outWriter.writerow([prop,street,'Leaseholder']) # Record them as a leaseholder
    else:
        outWriter.writerow([prop, street, 'Tenant']) # Record them as a tenant
    linkElem = browser.find_element_by_link_text('New enquiry')
    linkElem.click()  # follow the "New enquiry" link to start a new search
    time.sleep(waitTime)


# Main
# Set the path to the geckodriver (if using firefox)
browser = webdriver.Firefox(executable_path=r'C:\\Users\\CowsillB\\Downloads\\geckodriver-v0.20.0-win64\\geckodriver.exe')
browser.get('https://eservices.landregistry.gov.uk/www/wps/myportal/My_Home')

# Login to the service
loginEservices(username,pwd)

# Set up the output file and writer
outFile = open('properties.csv', 'w', newline='')
outWriter = csv.writer(outFile)

# Loop through each flat number in the flats list and determine whether or not they're leasehold
for prop in flats:
    searchSite(prop, street, town)
    leaseholdSearch(query)

# Close the file
outFile.close()