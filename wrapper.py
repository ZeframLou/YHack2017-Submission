import trends, reddit_handler, NN
from subprocess import run
import subprocess, sys
import numpy as np

def predict_tech(tech_name, owner):
    print('Running...')
    print('Doing sentiment analysis on Wikipedia page...')
    try:
        result = run("python ./pywikibot/pwb.py wiki_bot \"" + tech_name + "\"", stdout=subprocess.PIPE).stdout
        wiki_pol = float(result)
    except:
        print("Error: Technology not listed on Wikipedia, or is too short-lived.")
        exit(1)

    dates = trends.googleTrends(tech_name)
    start_date = int(dates[0])

    print('Fetching relevant US patents...')
    patent_count = trends.patentAPI(owner, tech_name, dates)

    print('Analyzing popularity on Reddit after technology gets initial momentum...')
    reddit_val_arr = reddit_handler.popularityCheck(tech_name, start_date)

    reddit_ratio = reddit_val_arr[0]
    reddit_pol = reddit_val_arr[1]
    reddit_sent = reddit_val_arr[2]

    sample = np.array([[reddit_ratio, reddit_pol, reddit_sent, patent_count, wiki_pol]], dtype=np.float32)
    print('Using Neural Network to predict probability of success...')
    print('Probability for success: ', NN.predict(sample) * 100, '%')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Error: not enough arguments')
        print('Usage: python wrapper.py "Technology Name" "Technology Leader"')
        exit(1)
    predict_tech(sys.argv[1], sys.argv[2])
