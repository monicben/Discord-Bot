import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client=discord.Client()

sad_words = ["down", "sad", "bad", "so down", "not confident", "ugly","depressed","mad"]

starter_compliments = ["You're a bad bitch. Chin up!","Don't say that, you're a confident queen", "Now you know better than putting yourself down! You're gorgeous!", "The Sun is jealous of how bright you shine!", "Inhale confidence, Exhale doubt.", "You are powerful, brilliant and brave!","Beauty begins the moment you decide to be yourself."]

if "responding" not in db.keys():
  db["responding"] = True

def get_compliment():
  response = requests.get("https://complimentr.com/")
  json_data = json.loads(response.text)
  compliment = json_data[0]['q']
  return(compliment)

def update_compliments(compliment_message):
  if "compliments" in db.keys():
    compliments = db["compliments"]
    compliments.append(compliment_message)
    db["compliments"] = compliments
  else:
    db["compliments"] = [compliment_message]

def delete_compliment(index):
  compliments = db["compliments"]
  if len(compliments) > index:
    del compliments[index]
    db["compliments"] = compliments


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith("$compliment me"):
    compliment = get_compliment()
    await message.channel.send(compliment)

  if db["responding"]:
    options = starter_compliments
    if "compliments" in db.keys():
      options = options + list(db["compliments"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    compliment_message = msg.split("$new ",1)[1]
    update_compliments(compliment_message)
    await message.channel.send("New compliment added!")

  if msg.startswith("$del"):
    compliments = []
    if "compliments" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_compliment(index)
      compliments = db["compliments"]
      await message.channel.send(compliments)

  if msg.startswith("$list"):
    compliments = []
    if "compliments" in db.keys():
      compliments = db["compliments"]
    await message.channel.send(compliments)

  if msg.startswith('$responding'):
    value = msg.split("$responding ",1)[1]

    if value.lower() =="true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
my_secret = os.environ['token1']
client.run(os.environ['token1'])




