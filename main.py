import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import pyttsx3
import webbrowser as wb
import time as time
import requests

WAKE_WORDS = ["hey shanana", "hey", "hello"]
newsapi = "7b968f61753c4c53a8b14deb0f71e0b4"
url = f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={newsapi}"
IsActive = False
fs = 40000
seconds = 5

recognizer = sr.Recognizer()


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1)

    engine.say(text)
    engine.runAndWait()


def record_audio():
    print("Speak now...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    time.sleep(0.3)

    # Convert float audio → PCM int16
    recording = np.int16(recording * 32767)

    write("recording.wav", fs, recording)


speak("Hey Basit!, I am Shanana Your voice Assistant , how may I help you")

while True:
    record_audio()
    try:
        with sr.AudioFile("recording.wav") as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio).lower()
        print("Shanana Thinks:", text)

        if any(word in text for word in WAKE_WORDS):
            speak("Yes Basit, I am listening")
            print("Shanana Thinks Correctly")
            time.sleep(3)
            IsActive = True
            continue
        if IsActive:

            if "youtube" in text:
                speak("Opening youtube")
            print("Opening youtube")
            time.sleep(3)
            wb.open("https://www.youtube.com/")
            IsActive = False

        elif "google" in text:
            time.sleep(0.5)
            speak("Opening google")
            time.sleep(1)
            wb.open("https://www.google.com/")
            IsActive = False

        elif "news" in text:
            speak("Here are the latest news")

            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [4])
                print(data)

                for article in articles:
                    print(article)
                    speak(article["title"])
                    IsActive = False

        elif "shutdown" in text:
            exit()

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Network error")
