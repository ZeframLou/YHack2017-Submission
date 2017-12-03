import trends, reddit_handler, NN
from subprocess import run
import subprocess, sys
import numpy as np
from easygui import *

def predict_tech(tech_name, owner):
    msgbox('Running...')
    msgbox('Doing sentiment analysis on Wikipedia page...')
    try:
        result = run("python ./pywikibot/pwb.py wiki_bot \"" + tech_name + "\"", stdout=subprocess.PIPE).stdout
        wiki_pol = float(result)
    except:
        msgbox("Error: Technology not listed on Wikipedia, or is too short-lived.")
        exit(1)

    dates = trends.googleTrends(tech_name)
    start_date = int(dates[0])

    msgbox('Fetching relevant US patents...')
    patent_count = trends.patentAPI(owner, tech_name, dates)

    msgbox('Analyzing popularity on Reddit after technology gets initial momentum...')
    reddit_val_arr = reddit_handler.popularityCheck(tech_name, start_date)

    reddit_ratio = reddit_val_arr[0]
    reddit_pol = reddit_val_arr[1]
    reddit_sent = reddit_val_arr[2]

    sample = np.array([[reddit_ratio, reddit_pol, reddit_sent, patent_count, wiki_pol]], dtype=np.float32)
    msgbox('Using Neural Network to predict probability of success...')
    prob = NN.predict(sample)
    msgbox('Probability for success: ' + str(prob * 100) + '%')
    return prob

if __name__ == '__main__':
    msg = "Enter a technology, and the leading company/organization in its development. The technology must have a Wikipedia page, and the entered name should exactly match the one on the Wiki page."
    title = "Trendline"
    fieldNames = ["Tech Name", "Tech Leader"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg, title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:  # do forever, until we find acceptable values and break out
        if fieldValues == None:
            break
        errmsg = ""

        # look for errors in the returned values
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        if errmsg == "":
            break  # no problems found
        else:
            # show the box again, with the errmsg as the message
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

    predict_tech(fieldValues[0], fieldValues[1])
