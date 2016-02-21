#!/usr/bin/env python
#
# Plant bot script that executes game and replies a score
#
import os.path
import shutil
import time
from TwitterClient import TwitterClient
import pyupm_i2clcd as lcd
import subprocess

def init_lcd(self):
  myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
  myLcd.clear()
  myLcd.setColor(0, 0, 255)
  myLcd.setCursor(0,0)

def start_game_lcd(self,twitter_name):
  myLcd.clear()
  myLcd.setCursor(1,0)
  myLcd.write("STARTING GAME")
  myLcd.setCursor(1,1)
  myLcd.write('twitter.com/@'+twitter_name)
  return

def game_score_lcd(self,game_score):
  myLcd.clear()
  myLcd.setCursor(1,0)
  myLcd.write('GAME OVER')
  myLcd.setCursor(1,1)
  myLcd.write('Score: '+game_score)
  return

if __name__ == '__main__':
  polling_interval = 30
  running = True
  twttr = TwitterClient.TwitterClient()
  # Set Color and init LCD
  init_lcd()

  while running:
    start = time.clock()
    games = os.listdir("newgames")

    for game_id in sorted(games):
      # Execute gameplay for gameid
      with open("newgames/"+str(game_id),"r") as game_file:
        player_name = game_file.readline()
      game_file.close()

      # Print twitter name to LCD
      start_game_lcd(player_name)

      # Execute game command and retrieve score
      game_score = os.popen('python ../Mario_Plant_Game/Mario_Plant_Game.py '+player_name).read()

      # Print Score to LCD
      game_score_lcd(player_name,game_score)

      with open("newgames/"+str(game_id),"a") as game_file:
        game_file.write(","+str(game_score)+"\n")
      game_file.close()

      twttr.reply_score(player_name,game_id,game_score)
      # Add Slack Reply

      # move to completed
      shutil.move("newgames/"+str(game_id),"completed/"+str(game_id))

    poll_duration = time.clock() - start
    time.sleep( polling_interval - poll_duration )
