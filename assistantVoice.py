import os
import speech_recognition
import speech_recognition as sr
import pyttsx3
import mysql.connector

WAKE = "hello assistant"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="pathdatabase"
)

mycursor = db.cursor()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = "".lower()

        try:
            said = r.recognize_google(audio)
            print(said)
        except speech_recognition.UnknownValueError:
            pass

    return said.lower()


firstList = []
a = True
while a:
    text = get_audio().lower()

    if text.count(WAKE) > 0:
        speak("Hello")
        mycursor.execute("SELECT name FROM filepaths")
        for x in mycursor:
            exe = str(x).lstrip("(").rstrip(")")
            exe3 = str(exe).rstrip(",")
            exe4 = str(exe3).lstrip('"').rstrip('"')
            exe5 = str(exe4).lstrip("'").rstrip("'")
            firstList.append(exe5.lower())
        text = get_audio().lower()
        if text.lower() in firstList:
            mycursor.execute("SELECT path FROM filepaths WHERE name = '" + text + "'")
            for x in mycursor:
                stripString1 = str(x).lstrip("(").rstrip(")")
                stripString2 = str(stripString1).rstrip(",")
                stripString3 = str(stripString2).lstrip('"').rstrip('"')
                stripString4 = str(stripString3).lstrip("'").rstrip("'")
                os.startfile(str(stripString4))
            speak("Opening" + text)
        elif not text:
            pass
        else:
            speak(text + " was not recognized")
            pass
