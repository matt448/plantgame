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

  def reply_score(self,player_name,tweet_id,game_score):
    self.api.PostUpdate("@"+player_name+" Score: "+str(game_score)+" Try again, guess a number for Level 2!", tweet_id)

  def tweet_top_scores(self,top_scores):
    top_score_string=""
    score_rank = 1
    for scores in top_scores[0:3]:
      top_score_string = top_score_string+" #"+str(score_rank)+" "+scores[2]+" Score: "+scores[0]
      score_rank+=1
    self.api.PostUpdate("Top Scores\n"+str(top_score_string))
