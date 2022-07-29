import os
import speech_recognition
import speech_recognition as sr
import pyttsx3
import sqlite3
import pygame
from tkinter import *

WAKE = "hello assistant"

mycursor = sqlite3.connect('Apps.db')


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
        exe = mycursor.execute("SELECT name FROM filepaths")
        for x in exe:
            exe = str(x).lstrip("(").rstrip(")")
            exe3 = str(exe).rstrip(",")
            exe4 = str(exe3).lstrip('"').rstrip('"')
            exe5 = str(exe4).lstrip("'").rstrip("'")
            firstList.append(exe5.lower())
        mylist = list(dict.fromkeys(firstList))
        text = get_audio().lower()
        if text.lower() in mylist:
            exe = mycursor.execute("SELECT path FROM filepaths WHERE name = '" + text + "'")
            for x in exe:
                stripString1 = str(x).lstrip("(").rstrip(")")
                stripString2 = str(stripString1).rstrip(",")
                stripString3 = str(stripString2).lstrip('"').rstrip('"')
                stripString4 = str(stripString3).lstrip("'").rstrip("'")
                try:
                    os.startfile(str(stripString4))
                except OSError as e:
                    root = Tk()
                    root.attributes('-topmost',
                                    True)  # Make error appear on top of screen, so it gets the user's attention
                    try:
                        photo = PhotoImage(file="backgrounds/error.ico")
                        root.iconphoto(False, photo)
                    except TclError:
                        pass  # Uses the default logo tkinter provides, in case user deletes `error.ico`.

                    root.title("ERROR")
                    app_width = 430
                    app_height = 70
                    screen_width = root.winfo_screenwidth()
                    screen_height = root.winfo_screenheight()
                    x = (screen_width / 2) - (app_width / 2)
                    y = (screen_height / 2) - (app_height / 2)
                    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
                    root.resizable(False, False)
                    pygame.mixer.init()
                    error_text = Label(root,
                                       text=text.capitalize() + " is either corrupted or an older version than the ones Windows supports.\n"
                                                                "Deleting this app from the voice assistant is recommended. ")

                    error_text.pack()

                    ok_button = Button(root, text="     OK     ", command=root.destroy, bg='grey')
                    ok_button.place(x=195, y=40)
                    pygame.mixer.music.load('errorSound.mp3')
                    pygame.mixer.music.play(loops=0)
                    root.mainloop()
                    break
                speak("Opening" + text)
        elif not text:
            pass
        else:
            speak(text + " was not recognized")
            pass
