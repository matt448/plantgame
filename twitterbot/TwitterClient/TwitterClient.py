#!/usr/bin/env python
import twitter

class TwitterClient():
  def __init__(self):
    self.api = twitter.Api(consumer_key='',
                      consumer_secret='',
                      access_token_key='',
                      access_token_secret='') 

  def get_players(self,game_id_offset):
    players = []
    # Retrieve only tweets newer than newest_tweet_id since last poll
    mentions = self.api.GetMentions(None,game_id_offset,None,0)

    if mentions:
      for s in mentions:
        # Add Levels filtering here
        if "play" in s.text.lower():
          players.append(s)
    return players

  def reply_to_player(self):
    print "reply to player"

  def tweet_scores(self):
    print "tweet scores"
