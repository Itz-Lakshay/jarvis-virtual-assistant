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
import logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    filename='jarvis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

conversation_history = [
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud, Give short responses please"}
]

MAX_HISTORY = 10  # keep last 10 exchanges to avoid unbounded growth


def aiProcess(command):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "I'm currently unable to reach my AI brain — no API key is configured."

    conversation_history.append({"role": "user", "content": command})

    # Trim history so it doesn't grow forever (keep system prompt + last N turns)
    if len(conversation_history) > MAX_HISTORY + 1:
        conversation_history[:] = [conversation_history[0]] + conversation_history[-MAX_HISTORY:]

    try:
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        reply = completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return "Sorry, I couldn't process that request right now."

def processCommand(c):
    logging.info(f"Command received: {c}")

    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        logging.info("Action: opened Google")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        logging.info("Action: opened LinkedIn")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        logging.info("Action: opened YouTube")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        logging.info("Action: opened Facebook")

    elif c.lower().startswith("play"):
        song = c.lower().split()[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
            logging.info(f"Action: played song '{song}'")
        else:
            speak(f"I don't have {song} in my music library.")
            logging.warning(f"Song not found: '{song}'")

    elif "time" in c.lower():
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        logging.info(f"Action: spoke time - {current_time}")

    elif "date" in c.lower():
        current_date = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
        logging.info(f"Action: spoke date - {current_date}")

    elif "news" in c.lower():
        if not newsapi:
            speak("News feature isn't configured right now.")
            logging.warning("News command failed: no API key configured")
            return
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:
                speak(article["title"])
            logging.info(f"Action: read {min(5, len(articles))} news headlines")
        else:
            logging.error(f"News API returned status {r.status_code}")

    else:
        output = aiProcess(c)
        speak(output)
        logging.info(f"AI response given for: '{c}'")


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
