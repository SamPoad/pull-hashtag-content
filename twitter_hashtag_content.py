'''This program will take an input of a Twitter hashtag, and return a csv file with the 
Twitter Users Name, Username, Date of Tweet, and the Text of the Tweet
for the last 7 days'''

# DEPENDENCIES
import tweepy # python library, documentation here: http://docs.tweepy.org/en/latest/index.html
import pandas as pd
from keyring import twitter_public_key, twitter_secret_key, twitter_public_access_token, twitter_secret_access_token

# build the engine that will allow for interaction with the API
auth = tweepy.OAuthHandler(twitter_public_key, twitter_secret_key)
auth.set_access_token(twitter_public_access_token, twitter_secret_access_token)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

# FUNCTIONS
# this function will download all the tweet text of a particular hashtag and write it to a csv
def creepy(hashtag):
    results = []
    # hashtag strip out the pound sign i'll add it myself
    for tweet in tweepy.Cursor(api.search,
        q=("#" + hashtag), # the search term from the getInput function
        lang = 'en', # as long as the tweet is in English
    ).items(): # adjust the arg passed to .items() to get a max number of tweets
        results.append([tweet.user.name, tweet.user.screen_name, tweet.created_at, tweet.text])
    output_df = pd.DataFrame(results,
        columns = [
            'Name',
            'ScreenName',
            'TweetDate',
            'TweetContent'
        ])
    output_df.to_csv(f'hashtag_content_{hashtag}.csv', sep = ',', index=False) # will save to your Current Working Directory
    print("Saved to CSV! File is named 'hashtag_content_x.csv' where x is the hashtag you searched.")

# this function gets user input, and calls creepy() using that input as an argument
def getInput():
    raw_input = input("What hashtag would you like to track? Note: Case-Sensitive\n")
    print("You entered " + raw_input)
    confirm = input("Is this correct? Press Y/N\n")
    if confirm.lower() == "y" or confirm.lower() == "yes":
        hashtag = raw_input.replace('#', '') # I'll add the pound sign back in myself, in case the user forgot to enter it themselves
        creepy(hashtag)
    else:
        getInput()


# RUN ME
getInput()