#!/usr/bin/env python
#
# Twitter polling script that retrieves players
#
import os.path
import shutil
import time
from TwitterClient import TwitterClient

if __name__ == '__main__':
  polling_interval = 600
  running = True
  twttr = TwitterClient.TwitterClient()
  score_list = []

  while running:
    start = time.clock()
    games = os.listdir("completed")

    for game_id in sorted(games):
      with open("completed/"+game_id,"r") as score_file:
        line = score_file.readline()
        user_and_score = line.split(',')
	score_list.append((user_and_score[1], game_id, "@"+user_and_score[0]))
      score_file.close()
    t1=sorted(score_list,key = lambda x: (x[1]))
    top_score_list=sorted(t1,key = lambda x: (x[0]),reverse=True)

    twttr.tweet_top_scores(top_score_list)

    poll_duration = time.clock() - start
    time.sleep( polling_interval - poll_duration )
