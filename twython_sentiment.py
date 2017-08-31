
# coding: utf-8

# In[21]:


import pandas as pd
from twython import Twython, TwythonRateLimitError, TwythonError
from time import sleep
import itertools


# In[2]:


import pandas as pd
from twython import Twython, TwythonRateLimitError, TwythonError
from time import sleep
import itertools


# In[20]:



APP_KEY = '2701n8yQhIWIGWeld9Pg1pCzo'
APP_SECRET = 'wi9V8ejZdl7MhW8S1Xv2bzqwry8AamEugU0LMFb1w0gxS4imgL'
OAUTH_TOKEN = '104434883-8GlZB2wm7Vn3XKakFBnPlXl2ktgQWTpqC462gTW4'
OAUTH_SECRET = '8nOct9wjzZ8bCgrWbttRW1ksoRXwpOOXqs8c5uuF7ZmPy'

csv_path = 'tweet_ids_and_sentiments.csv'


# In[3]:


def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page


# In[4]:


def get_twython_client():
    return Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

def get_twitter_posts_from_list(client, post_id_list):
    return client.lookup_status(id=post_id_list)

def get_all_tweets(csv_path):
    tweet_ids_and_sentiments = pd.read_csv(csv_path)
    
    twitter_client = get_twython_client()

    pages = list(paginate(tweet_ids_and_sentiments.tweet_id, 100))

    all_tweets = []

    for page in pages:
        try:
            posts = get_twitter_posts_from_list(twitter_client, page)
        except TwythonRateLimitError as e:
            print 'Whoops, we exceeded the rate limit somehow. Pausing for 15 minutes...'
            sleep(15 * 60 + 1)
            posts = get_twitter_posts_from_list(twitter_client, page)
        except TwythonError as e:
            print e

        all_tweets += posts
        print 'got %d posts from page %d...' % (len(posts), pages.index(page) + 1)
    print 'got all pages - %d posts in total' % (len(all_tweets))
    return all_tweets, tweet_ids_and_sentiments


# In[7]:


def get_tweet_dataframe(all_tweets, tweet_ids_and_sentiments):
    # List comprehension to grab just the text and ID
    relevant_tweet_info = [
        {
            'text':t['text'],
            'tweet_id':t['id']
        } for t in all_tweets
    ]
  # Turning that list into a dataframe so it can be merged with the dataframe that has the sentiment of each post
    tweet_texts = pd.DataFrame(relevant_tweet_info)
    df = pd.merge(tweet_ids_and_sentiments, tweet_texts)    
    return df


  


# In[9]:


def fetch_the_data():
    all_tweets , tweet_ids_and_sentiments = get_all_tweets(csv_path)
    df = get_tweet_dataframe(all_tweets, tweet_ids_and_sentiments)
    return df


# In[18]:


#return search results

from twython import Twython, TwythonError


twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
try:
    search_results = twitter.search(q='WebsDotCom', count=50)
except TwythonError as e:
    print e

for tweet in search_results['statuses']:
    print 'Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'),
                                       tweet['created_at'])
print tweet['text'].encode('utf-8'), '\n'


# In[19]:


from twython import TwythonStreamer


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')
        # Want to disconnect after the first result?
        # self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data

# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_SECRET)

stream.statuses.filter(track='twitter')
# stream.user()
# Read the authenticated users home timeline
# (what they see on Twitter) in real-time
# stream.site(follow='twitter')


# In[22]:


#get user time line

from twython import Twython, TwythonError

# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
try:
    user_timeline = twitter.get_user_timeline(screen_name='Chris Albon')
except TwythonError as e:
    print e

print user_timeline


# In[31]:


#getting trends

from twython import Twython
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

result = twitter.get_place_trends(id = 23424977)

if result:
    for trend in result[0].get("trends", []):
        
                                                print("{0} \n".format(trend["name"]))


# In[ ]:




