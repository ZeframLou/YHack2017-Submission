from pytrends.request import TrendReq
import time
import datetime
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re

pytrends = TrendReq(hl='en-US', tz=360)


def googleTrends(keyword):
    kw_list = []
    return_list = []
    kw_list.append(keyword)
    pytrends.build_payload(kw_list, cat=0, timeframe='all', geo='US', gprop='')
    interest_over_time_df = pytrends.interest_over_time()
    interest_over_time_df[keyword] = interest_over_time_df[keyword].rolling(window=5).mean()
    # interest_over_time_df.plot()
    for x in range(0, len(interest_over_time_df)):
        if interest_over_time_df[keyword].iloc[x] >= 25:
            # print(interest_over_time_df.index[x])
            return_list.append(time.mktime(interest_over_time_df.index[x].timetuple()))
            # time.mktime(d.timetuple())
            leftBound = x
            break
    for y in range(leftBound + 1, len(interest_over_time_df)):
        if interest_over_time_df[keyword].iloc[y] <= 25:
            # print(interest_over_time_df.index[y])
            return_list.append(time.mktime(interest_over_time_df.index[y].timetuple()))
            rightBound = y
            break
        elif len(return_list) == 1:
            return_list.append(time.mktime(datetime.datetime.now().timetuple()))
    return return_list



#Function to build a URL based on the company/keywords
def patentURL(company, keyword, time):
    #Converts space to something HTML can handle
    company = company.replace(" ", "%20")
    keyword = keyword.replace(" ", "%20")
    
    BASE_URL = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query="
    
    #Builds URL given specified input values and returns it
    URL = BASE_URL + "AN%2F%22" + company + "%22+AND%0D%0ASPEC%2F%22" + keyword + "%22+AND%0D%0AISD%2F20040101-%3E" + time[1] + "&d=PTXT"
    return URL

#Functions which crawls the USPTO website given the specified query inputs, and returns the number of granted patents    
def patentAPI(company, keyword, time):
    #Converts datetime() format to string
    stringTime = []
   
    #pass the year, month, and year into a YYYYMMDD format as a string, to pass into the URL
    for x in range(0, len(time)):
        time[x] = datetime.datetime.fromtimestamp(time[x])
        stringTime.append(str(time[x].year))
        if time[x].month < 10:
            stringTime[x] += "0" + str(time[x].month)
        else:
            stringTime[x] += str(time[x].month)
        
        if time[x].day < 10:
            stringTime[x] += "0" + str(time[x].day)
        else:
            stringTime[x] += str(time[x].day)
            
        
    #print(stringTime[1])
    
    #Grabs URL from above function
    URL = patentURL(company, keyword, stringTime)
    #print(URL)
    #Creates static variable to search in order to verify there are no patents
    NO_PATENTS = "No patents have matched your query"    
    
    #Open up the URL with urllib2 as a Python User-Agent
    req = urllib2.Request(URL, headers={'User-Agent' : "python"})
    _file = urllib2.urlopen(req)
    
    #Read the HTML from the given URL, and parse the HTML
    patent_html = _file.read()
    soup = BeautifulSoup(patent_html, 'html.parser')
    
    #Extract numbers from bolded text
    patent_data = soup.findAll("strong")
    numbers = [d.text for d in patent_data]
    
    #If NO_PATENTS string found, then return 0
    if soup.findAll(text=re.compile('No patents have matched your query')):
        return 0
    #If a number of patents is found, extract the last bolded number and return it
    elif soup.findAll(text=re.compile(' out of ')):
        return numbers[2]
    #Otherwise, the website redirected us to a specific patent, so return 1
    else:
        return 1
