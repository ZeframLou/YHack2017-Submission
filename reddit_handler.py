import praw
from textblob import TextBlob

reddit = praw.Reddit(
client_id='example_id',
client_secret="example_secret",
user_agent='script by /u/reddit_user',
)

# TODO Also normalize and add Subjectivity

'''
Takes in:
@param phrase: The string we search for
@param date1: The start date
@param date2: The end date

@return hits: The number of reddit posts which match the phrase
'''
def popularity (phrase, date1, date2, minWordLength = 5):

    # Mod value (we only record every nth value):
    n = 5

    # Number of values we parse:
    hits = 1

    # Subreddit holder array
    subredditArr = []

    # Submission holder array (unused for now)
    # submissionArr = []

    # Array for answer:
    answerArr = []

    # Helpful temp vars:
    avgKarma = 0
    avgPolarity = 0
    avgSubjectivity = 0

    # Temporary holder arrays
    tempKarmaArr = []
    tempPolarityArr = []
    tempSubjectivityArr = []

    # Initialize subreddits
    # subredditArr.append(reddit.subreddit('futurology'))
    subredditArr.append(reddit.subreddit('technology'))

    # Iterate through subreddit array
    for i in range(len(subredditArr)):

        # Set count to be 0
        count = 0

        # For each submission in the subreddit:
        for submission in subredditArr[i].submissions(date1, date2):

            # If it matches our key phrase, and it's also the nth submission:
            if phrase in submission.title.lower() and len(submission.title.split()) > minWordLength and (count % n == 0):

                tempKarma = submission.score
                # submissionArr[0].append(tempKarma)
                avgKarma += tempKarma
                print(tempKarma)

                tempPolarity = TextBlob(submission.title).sentiment.polarity
                # submissionArr[1].append(tempPolarity)
                avgPolarity += tempPolarity
                print(tempPolarity)

                tempSubjectivity = TextBlob(submission.title).sentiment.subjectivity
                # submissionArr[2].append(tempSubjectivity)
                avgSubjectivity += tempSubjectivity
                print(tempSubjectivity)

                # Used only for logging
                # print(repr(submission.title) + " " + get_date(submission))

                # Update hits
                hits += 1

            # Update count
            count += 1

        # Set hits back to 1:
        hits = 1

        # Normalize the karma values
        answerArr.append((avgKarma/hits)/subredditArr[i].subscribers)
        # avgKarma = 0

        # Normalize the polarity values
        # tempPolarityArr.append(avgPolarity/hits)
        answerArr.append(avgPolarity/hits)
        # avgPolarity = 0

        # Normalize the subjectivity values
        # tempSubjectivityArr.append(avgSubjectivity/hits)
        answerArr.append(avgSubjectivity/hits)
        # avgSubjectivity = 0

        '''
        # Average out the average Karma values:
        for i in range(len(tempKarmaArr)):
            avgKarma += tempKarmaArr[i]
        answerArr[0].append(avgKarma/len(tempKarmaArr))

        # Average out the average Polarity values
        for i in range(len(tempPolarityArr)):
            avgPolarity += tempPolarityArr[i]
        answerArr[1].append(avgPolarity/len(tempPolarityArr))

        # Average out the average Subjectivity values;
        for i in range(len(tempSubjectivityArr)):
            avgSubjectivity += tempSubjectivityArr[i]
        answerArr[2].append(avgSubjectivity/len(tempSubjectivityArr))
        '''

    return answerArr



def popularityCheck(phrase, date1, flag = True, minWordLength = 5):
    # Number of values we parse:
    hits = 1

    #Average temp vars:
    avgKarma = 0
    avgPolarity = 0
    avgSubjectivity = 0

    # Subreddit holder array
    subredditArr = []

    # Answer array:
    answerArr = []

    if (flag == True):
        # Populate subreddit holder array
        subredditArr.append(reddit.subreddit('technology'))
        # Unix one year in seconds, value
        time_chunk = 86400 * 14
    else:
        # Grab values from r/all
        subredditArr.append(reddit.subreddit('all'))
        # Unix one year in seconds, value
        time_chunk = 86400 * 1

    # Iterate through subreddit array
    # for i in range(len(subredditArr)):

    # For each submission in the subreddit:
    for submission in subredditArr[0].submissions(date1, date1 + time_chunk):

        # If it matches our key phrase, and it's also the nth submission:
        if phrase.lower() in submission.title.lower() and len(submission.title.split()) > minWordLength:

            # print(repr(submission.title) + " " + get_date(submission))

            tempKarma = submission.upvote_ratio
            avgKarma += tempKarma

            tempPolarity = TextBlob(submission.title).sentiment.polarity
            avgPolarity += tempPolarity

            tempSubjectivity = TextBlob(submission.title).sentiment.subjectivity
            avgSubjectivity += tempSubjectivity

            # Update hits
            hits += 1

    answerArr.append(avgKarma/hits)
    answerArr.append(avgPolarity/hits)
    answerArr.append(avgSubjectivity/hits)
    answerArr.append(hits)

    return answerArr
