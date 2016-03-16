from bs4 import BeautifulSoup
import requests
import re

# Base URL
# urlString = 'http://anchorage.craigslist.org/w4w/4831615865.html'

def scrape_craigslist(urlString):
    soup = BeautifulSoup(requests.get(urlString).text)

    # Email URL
    cityIndex = urlString.find('.org/') + 5
    cityString = urlString[0:cityIndex]
    idString = urlString[cityIndex:]
    idString = idString[0:idString.find('.')]
    urlString = cityString + "reply/" + idString

    # Get email
    r  = requests.get(urlString)
    email = r.text
    searchObj = re.search( r'class="mailapp"> (.*)', email, re.M|re.I)
    email = searchObj.group()
    email = email[17:]
    orgIndex = email.find('.org') + 4
    email = email[0:orgIndex]

    craig_title = str(soup.find_all("h2", class_="postingtitle")[0]).split("</span>")[-1].strip()[:-6]

    #Print email
    return email, craig_title
