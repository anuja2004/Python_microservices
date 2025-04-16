import os
import speech_recognition as sr

# Suppress ALSA errors
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["ALSA_LOG"] = "0"
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.info=false"

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again, please.")
        return "None"
    return query

while True:
    user_input = takeCommand().lower()
    if user_input == "exit":
        print("Exiting...")
        break
