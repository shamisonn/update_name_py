# -*- coding: utf-8 -*-
__author__ = 'shamison'

from twitter import *
import configparser
import os

# config.iniから読み込み. consumer_keyとかを諸々書いておく
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config/config.ini'))
oauth_config = config['oauth']

# userstream用に作成.
oauth = OAuth(
    consumer_key=oauth_config['consumer'],
    consumer_secret=oauth_config['consumer_secret'],
    token=oauth_config['token'],
    token_secret=oauth_config['token_secret']
)

# ツイートやらプロフィールを取ってくるため作成
tw = Twitter(
    auth=OAuth(
        oauth_config['token'],
        oauth_config['token_secret'],
        oauth_config['consumer'],
        oauth_config['consumer_secret'])
)

# screen_nameを記憶
my_name = '@' + tw.account.settings()['screen_name']

# 現在の名前を表示
print("現在の名前: " + tw.account.verify_credentials()['name'])

# user_streamをする.
tw_us = TwitterStream(auth=oauth, domain='userstream.twitter.com')

# update_nameの実装
def update_name(msg):
    # tweetの文字列の加工
    new_name = msg['text']
    new_name = new_name.replace(my_name + ' ', '')
    
    # 先頭から20文字を名前に指定する
    new_name = new_name[0:20]
    tw.account.update_profile(name=new_name)
    print("名前を変更しました: -> " + new_name)

# tweetを取得する.
for msg in tw_us.user():
    if "friends" in msg:
        continue
    elif "delete" in msg:
        continue

    # タイムラインの表示
    # if "user" in msg:
    # print("@"+msg['user']['screen_name']+" : "+msg['user']['name']+' '+msg['text'])

    # update_nameするかを判定.
    # 特定の文字列が流れてきたらupdate_nameする.
    if "text" in msg and (msg['text'].startswith(my_name + ' ')):
        update_name(msg)
