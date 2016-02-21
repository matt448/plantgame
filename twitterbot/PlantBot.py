#!/usr/bin/env python
#
# Plant bot script that executes game and replies a score
#
import os.path
import shutil
import time
from TwitterClient import TwitterClient
import subprocess

if __name__ == '__main__':
  polling_interval = 30
  running = True
  twttr = TwitterClient.TwitterClient()

  while running:
    start = time.clock()
    games = os.listdir("newgames")

    for game_id in sorted(games):
      # Execute gameplay for gameid
      with open("newgames/"+str(game_id),"r") as game_file:
        player_name = game_file.readline()
      game_file.close()
      
      # Execute game command and retrieve score
      game_score = os.popen('python ../Mario_Plant_Game/Mario_Plant_Game.py '+player_name).read()
       
      with open("newgames/"+str(game_id),"a") as game_file:
        game_file.write(","+str(game_score)+"\n")
      game_file.close()

      twttr.reply_score(player_name,game_id,game_score)
      # Add Slack Reply

      # move to completed
      shutil.move("newgames/"+str(game_id),"completed/"+str(game_id))

    poll_duration = time.clock() - start
    time.sleep( polling_interval - poll_duration )
