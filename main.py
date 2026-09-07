import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

Recognizer = sr.Recognizer()

newsapi = os.environ.get("NEWS_API_KEY")

def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the mp3 file
    pygame.mixer.music.play()

    # Keeps the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('temp.mp3')

def aiProcess(command):
    client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY")
    )

    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud, Give short responses please"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif c.lower().startswith("play"):
        song = c.lower().split()[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "time" in c.lower():
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "date" in c.lower():   
        current_date = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the json response
            data = r.json()

            # Extract the articles
            articles = data.get('articles',[])

            # Speak the headline
            for article in articles:
                speak(article["title"])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    
    speak("Initializing Jarvis....")

    while True:
        # Listen for the wake word "Jarvis"
        # Obtain the audio from microphone
        r = sr.Recognizer()

        # Recognize speech using google
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout = 3,phrase_time_limit = 1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Word Detected")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source,timeout = 7,phrase_time_limit = 5)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("Error: {0}".format(e))
