![Trendline](https://i.imgur.com/qnPNMKp.png)

<hr/>

Trendline is a tool that tries to predict future success of current tech by relying on the powers of machine learning and induction.

## Prerequisites
* Python 3.5.4
* Tensorflow
* numpy
* pytrends
* praw
* textblob
* panda
* urllib
* BeautifulSoup
* requests
* easygui

## Usage
Under the root directory, enter the following code into the command line:
```
    python NN.py
    python wrapper.py
```
Then, enter the required information into the new window.
**"Technology Name"** is the name of the tech you wish to get info about (e.g. blockchain, iPhone, Windows 10).
**"Technology Leader"** is the name of the company associated with the technology (e.g. ConsenSys, Apple, Microsoft).

## The code:
At the heart of it, Trendline uses:

1) The Python Reddit API Wrapper (PRAW) to query for submissions that relate to a topic

2) Pytrends API to gauge how interest in a topic is developing over time via Google Trends.

3) WikiBot to traverse Wikipedia pages.

4) US Patent Office data and Beautiful Soup to parse patent records.

5) TextBlob to perform sentiment analysis on selected text.

6) TensorFlow for the actual functional approximation.

<hr/>

![Trendline diagram](https://i.imgur.com/1xt5QZg.png)
