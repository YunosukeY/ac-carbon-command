#!/usr/bin/env python3
import os
import sys
import re
import json
import webbrowser
import random
import requests
from urllib import request, parse
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv

def url_validation(url):
  m = re.fullmatch(r'https://atcoder.jp/contests/\w+/submissions/\d+(\?lang=(ja|en))?', url)
  if m == None:
    return False
  else:
    return True

def get_submission_id(url):
  tmp = re.split('[/?]', url)
  if tmp[-1][0:4] == 'lang':
    return tmp[-2]
  else:
    return tmp[-1]

def get_soup(submission_url):
  html = request.urlopen(submission_url)
  soup = BeautifulSoup(html, 'html.parser')
  return soup

def get_submission_code(soup, submission_url):
  submission_code = soup.find(id='submission-code').get_text()
  return submission_code

def get_language(soup, submission_url):
  lang = soup.find_all(class_='text-center')[3].get_text()
  return lang

def get_lang_para(lang):
  d = {'C (GCC 9.2.1)': 'text/x-csrc',
      'C (Clang 10.0.0)': 'text/x-csrc',
      'C++ (GCC 9.2.1)': 'text/x-c++src',
      'C++ (Clang 10.0.0)': 'text/x-c++src',
      'Java (OpenJDK 11.0.6)': 'text/x-java',
      'Python (3.8.2)': 'python',
      'Ruby (2.7.1)': 'ruby',
      'C# (.NET Core 3.1.201)': 'text/x-csharp',
      'PyPy3 (7.3.0)': 'python',
      'Haskell (GHC 8.8.3)': 'haskell',
      'Rust (1.42.0)': 'rust',
      'Brainfuck (bf 20041219)': 'auto'
      }
  if lang in d:
    return d[lang]
  else:
    return 'auto'

def get_carbon_image(code, lang):
  headers = {'Content-Type' : 'application/json'}
  obj = {'code' : code, 'language': lang} 
  json_data = json.dumps(obj).encode('utf-8')
  carbon_url = 'https://carbonara.now.sh/api/cook'
  res = requests.post(carbon_url, json_data, headers = headers)
  image = res.content
  return image

def get_media_id(twitter, image):
  media_upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
  files = {'media' : image}
  res = twitter.post(media_upload_url, files = files)
  if res.status_code != 200:
    print('Can\'t upload media')
    exit()
  media_id = json.loads(res.text)['media_id_string']
  return media_id

def get_tweet_status(submission_id):
  return 'submission: ' + submission_id + '\n' + str(random.randrange(1000000000)) + '(rand)'

def get_display_url(twitter, media_id, submission_id):
  post_tweet_text = 'https://api.twitter.com/1.1/statuses/update.json'
  status = get_tweet_status(submission_id)
  params = {'status': status, 'media_ids': media_id}
  res = twitter.post(post_tweet_text, params = params)
  if res.status_code != 200:
    print('Can\'t post tweet')
    exit()
  display_url = json.loads(res.text)['entities']['media'][0]['display_url']
  return display_url

def get_tweet_title(soup, submission_url):
  tweetinfo = soup.find(class_='a2a_kit')
  tweet_title = tweetinfo.get('data-a2a-title') + ' ' + tweetinfo.get('data-a2a-url')
  return tweet_title

def tweet(tweet_title, display_url):
  open_twitter_url = 'https://www.addtoany.com/add_to/twitter?linkurl=' + parse.quote(display_url) + '&linkname=' + parse.quote(tweet_title) + '&linknote='
  webbrowser.open(open_twitter_url)

def load_env():
  load_dotenv()
  API_KEY = os.getenv('API_KEY')
  API_KEY_SECRET = os.getenv('API_KEY_SECRET')
  ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
  ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
  return API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def get_twitter():
  API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = load_env()
  twitter = OAuth1Session(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  return twitter

if __name__ == '__main__':
  args = sys.argv
  if len(args) < 2:
    exit()
  submission_url = args[1]
  if url_validation(submission_url) == False:
    print('Invalid URL')
    exit()

  soup = get_soup(submission_url)
  submission_code = get_submission_code(soup, submission_url)
  language = get_language(soup, submission_url)
  lang_para = get_lang_para(language)
  
  image = get_carbon_image(submission_code, lang_para)

  twitter = get_twitter()
  media_id = get_media_id(twitter, image)
  display_url = get_display_url(twitter, media_id, get_submission_id(submission_url))
  
  tweet_title = get_tweet_title(soup, submission_url)
  tweet(tweet_title, display_url)
