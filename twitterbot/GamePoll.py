#!/usr/bin/env python
#
# Twitter polling script that retrieves players
#
# requires python_twitter
# pip install python_twitter
#

import os.path
import time
from TwitterClient import TwitterClient 

def get_game_requests(twttr,last_tweet_id):
  game_requests = {}
  players = twttr.get_players(last_tweet_id)
  for t in players:
    game_requests[t.id] = t.user.screen_name
  return game_requests

def save_game_requests(game_requests):
  for game in game_requests:
    with open("newgames/"+str(game),'w') as f:
      f.write(game_requests[game])
    f.close()

if __name__ == '__main__':
  polling_interval = 61 # once per minute
  running = True
  twttr = TwitterClient.TwitterClient()
  # read game id offset from file 
  if os.path.exists("game_id_offset"):
    offset_file = open("game_id_offset","r")
    game_id_offset = int(offset_file.readline())
    offset_file.close() 
  else:
    game_id_offset = 1

  while running:
    start = time.clock()
    game_requests = get_game_requests(twttr,game_id_offset)

    if game_requests:
      game_ids = sorted(game_requests.keys(), reverse=True)
      # Save most recent tweet as offset for next poll
      if game_ids[0]:
        game_id_offset = game_ids[0]
        #persist game id offset for restart
        with open("game_id_offset","w") as save_offset_file:
            save_offset_file.write(str(game_id_offset))
        save_offset_file.close()

      save_game_requests(game_requests)

    poll_duration = time.clock() - start
    time.sleep( polling_interval - poll_duration )
