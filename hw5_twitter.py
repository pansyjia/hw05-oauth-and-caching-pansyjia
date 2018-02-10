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
# requests.get(url, auth = auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this


#Code for Part 1:Get Tweets
params = { "screen_name": username, "count": num_tweets}
response = requests.get(url, params=params, auth=auth)
# print(response.text)
resp_file = "tweets.json"
f = open(resp_file, "w")
resp_dict = json.loads(response.text)
resp_str = json.dumps(resp_dict)
f.write (resp_str)
f.close()

#Code for Part 2:Analyze Tweets
for tweet in resp_dict["statuses"]:
    tokenized_text = nltk.word_tokenize(tweet["text"])
    words_dict = nltk.FreqDist(tokenized_text)

words_lst = []
stopwords_lst = ["http", "https", "RT"]

for tweet in resp_dict["statuses"]:
    tokenized_text = nltk.word_tokenize(tweet["text"])
    for word in tokenized_text:
        if word[0].isalpha() and word not in ignore_lst:
            words_lst.append(word)
        else:
             print("Not a word: " + str(word))
             continue

words_dict = nltk.FreqDist(words_lst)


sorted_words_lst = sorted(words_dict.items(), key = lambda x: x[1], reverse = True)

print("THE 5 MOST FREQUENTLY USED WORDS: ")
for word_tuple in sorted_words_lst[0:5]:
    word, frequency = word_tuple 
    print(word, ":", frequency, "times")


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
