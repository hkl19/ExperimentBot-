

## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr     # import the library
import subprocess
from gtts import gTTS
import os
import pygame

# sender = input("What is your name?\n")
# Define the command to play the sound

bot_message = ""
message=""
ID = "000"
count = 0


while bot_message != "end the survey":

    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            print("You said : {}".format(message))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue
    print("Sending message now...")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    print("Bot says, ",end=' ')
    for i in r.json():
        count += 1
        bot_message = i['text']
        print(f"{bot_message}")

    myobj = gTTS(text=bot_message)
    myobj.save(ID+"_"+str(count)+".mp3")
    print("saved")
    # Playing the converted file
    pygame.init()
    pygame.mixer.music.load(ID+"_"+str(count)+".mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)