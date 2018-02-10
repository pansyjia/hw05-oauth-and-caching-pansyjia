from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk

## SI 507 - HW05
## Name: Siyu Jia (uniqname: siyujia)
## Your section day/time: 009 (Jie-wei Wu)
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth = auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this
CACHE_FNAME = "twitter_cache.json"

## check if data is fetched from the cache
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_json = cache_file.read()
    CACHE_DICTION = json.loads(cache_json)
    cache_file.close()
except:
    CACHE_DICTION = {}

## generate a unique id
def params_unique_combination(base_url, params_dict):
    alphabetized_keys = sorted(params_dict.keys())

    res = []
    for key in alphabetized_keys:
        res.append("{}-{}".format(key, params_dict[key]))
    return base_url + "_".join(res)


## get data from cached file or Twitter
def get_from_twitter(username, num_tweets):

    base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params_dict = {}
    params_dict["screen_name"] = username
    params_dict["count"] = num_tweets

    unique_ident = params_unique_combination(base_url, params_dict)

    if unique_ident in CACHE_DICTION:
        print("Fetching cahced data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Fetching data from Twitter...")
        response = requests.get(url = base_url, params = params_dict, auth = auth)
        resp_lst = json.loads(response.text) #resp_lst is a list of dictionaries(tweets)
        

        resp_dict = {}
        resp_dict["statuses"] = resp_lst
        CACHE_DICTION[unique_ident]= resp_dict

        write_file = open(CACHE_FNAME, 'w')
        write_file.write(json.dumps(CACHE_DICTION))
        write_file.close()
        return CACHE_DICTION[unique_ident]



#Code for Part 1:Get Tweets
######## get user tweets ########
# params = { "screen_name": username, "count": num_tweets}
# response = requests.get(url, params=params, auth = auth)
# print(response.text)
results_dict = get_from_twitter(username, num_tweets)

## write the json to a file
# resp_file = "tweets.json"
# f = open(resp_file, "w")
# resp_str = json.dumps(results_dict, indent = 2)
# f.write (resp_str)
# f.close()



#Code for Part 2:Analyze Tweets
# for tweet in results_dict["statuses"]:
#     tokens = nltk.word_tokenize(tweet["text"])
#     words_dict = nltk.FreqDist(tokens)

words_lst = []
stopwords_lst = ["http", "https", "RT"]

for tweet in results_dict["statuses"]:
    tokens = nltk.word_tokenize(tweet["text"])
    for word in tokens:
        if word[0].isalpha() and word not in stopwords_lst:
            words_lst.append(word)

words_dict = nltk.FreqDist(words_lst)

sorted_words_lst = sorted(words_dict.items(), key = lambda x: x[1], reverse = True)

print("THE 5 MOST FREQUENTLY USED WORDS: ")
for word_tuple in sorted_words_lst[0:5]:
    word, frequency = word_tuple
    print(word, ": ", frequency, "times")


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
