import pywikibot
import sys
import trends
from textblob import TextBlob

ONE_MONTH = 3000000


def print_tech_polarities(techs):
    for tech in techs:
        lifespan = trends.googleTrends(tech)
        page = old_page(tech, int(lifespan[0]))
        try:
            print(TextBlob(page.text).sentiment.polarity, end='')
        except:
            exit(1)


def old_page(page_name, start_time):
    pages = pywikibot.Page(site, page_name).revisions(content=True, starttime=start_time, endtime=start_time + ONE_MONTH * 2, reverse=True)
    for page in pages:
        return page


if __name__ == '__main__':
    site = pywikibot.Site('en', 'wikipedia')
    print_tech_polarities(sys.argv[1:])
