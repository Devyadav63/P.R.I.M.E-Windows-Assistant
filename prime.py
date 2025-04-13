# SURYA- Smart Unified Response for Your Assistance
import speech_recognition as sr
import os
import webbrowser
import datetime
import wikipedia
import pyttsx3
import openai
import time
import pywhatkit
from Shot import Take_Shot
from Gemini_API import Answer

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 195)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def chatai(query):
    speak(Answer(query))
    print(Answer(query))


def Listenme():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"you said: {query}\n")
    except Exception as e:
        # print(e)
        print("Say that again please...")

        return "None"  # None string will be returned
    return query


def Listenmeque():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"you said: {query}\n")
    except Exception as e:
        # print(e)
        print("Say that again please...")

        return "None"  # None string will be returned
    return query


def Listenmeai():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        # print(e)
        print("Say that again please...")

        return "None"  # None string will be returned
    return query


def decrease_volume():
    pyautogui.press("volumedown")


def increase_volume():
    pyautogui.press("volumeup")


def remindme():
    pass


import ctypes

# Define the media control commands

# Call the function to play or pause media
import ctypes

# Define the media control command for pause
from ocr_read import ocr_extracter
import pyautogui


def play():
    # Simulate pressing the "play/pause" media key
    pyautogui.press('playpause')


#

def next_track():
    pyautogui.press("nexttrack")


def previous_track():
    pyautogui.press("prevtrack")


if __name__ == '__main__':
    print('Welcome Dev Sir')
    # speak("Smart Unified Response for Your Assistance, Surya A I activated Sir")
    while True:

        query = Listenme()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["gmail", "https://mail.google.com/mail/u/0/#inbox"],
                 ["email", "https://mail.google.com/mail/u/0/#inbox"],
                 ["inbox", "https://mail.google.com/mail/u/0/#inbox"], ["instagram", "https://www.instagram.com/"],
                 ["instagram inbox", "https://www.instagram.com/direct/inbox/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "bye".lower() in query.lower():
            exit()
        elif "Bye".lower() in query.lower():
            exit()
        elif "exit" in query:
            exit()
        elif "Exit" in query:
            exit()

        elif "initiate advance" in query:
            speak("Advanced Surya A I ,powered by Google Gemini, initiated sir")
            while True:
                query = Listenmeai()
                if "close advance" in query:
                    break
                else:
                    print("Chatting...")
                    chatai(query)

        elif "initiate advanced" in query:
            speak("Advanced Surya A I ,powered by Google Gemini, initiated sir")
            while True:
                query = Listenmeai()
                if "close advanced" in query:
                    break
                else:
                    print("Chatting...")
                    chatai(query)
        elif "start Gemini" in query:
            speak("Advanced Surya A I ,powered by Google Gemini, initiated sir")
            while True:
                query = Listenmeai()
                if "close Gemini" in query:
                    break
                else:
                    print("Chatting...")
                    chatai(query)
        elif "generate code" in query:
            speak("Please tell me the question sir")
            qu = Listenmeque()
            speak(f"Code Generation process for the question {qu} has been started sir")
            res = Answer(qu)
            speak(
                "Code Generation Completed, Do you want me to write it for you, say write code whenever you want, else say, delete it")
            file = open("Generated_Code.txt", "w")
            file.write(res)
            file.close()

        elif "generate a code" in query:
            speak("Please tell me the question sir")
            qu = Listenmeque()
            speak(f"Code Generation process for the question {qu} has been started sir")
            res = Answer(qu)
            speak(
                "Code Generation Completed, Do you want me to write it for you, say write code whenever you want, else say, delete it")
            file = open("Generated_Code.txt", "w")
            file.write(res)
            file.close()

        elif "write the code" in query:
            speak("Ok sir code writing will start in ")
            for i in range(5, 0, -1):
                time.sleep(0.5)
                speak(i)
            file = open("Generated_Code.txt", "r")
            response_extracted = file.read()
            file.close()
            pyautogui.typewrite(response_extracted)
            speak("Code Writing is Completed sir")
        elif "write a code" in query:
            speak("Ok sir code writing will start in ")
            for i in range(5, 0, -1):
                time.sleep(0.5)
                speak(i)
            file = open("Generated_Code.txt", "r")
            response_extracted = file.read()
            file.close()
            pyautogui.typewrite(response_extracted)
            speak("Code Writing is Completed sir")
        elif "write a generated code" in query:
            speak("Ok sir code writing will start in ")
            for i in range(5, 0, -1):
                time.sleep(0.5)
                speak(i)
            file = open("Generated_Code.txt", "r")
            response_extracted = file.read()
            file.close()
            pyautogui.typewrite(response_extracted)
            speak("Code Writing is Completed sir")
        elif "write code" in query:
            speak("Ok sir code writing will start in ")
            for i in range(5, 0, -1):
                time.sleep(0.5)
                speak(i)
            file = open("Generated_Code.txt", "r")
            response_extracted = file.read()
            file.close()
            pyautogui.typewrite(response_extracted)
            speak("Code Writing is Completed sir")

        elif "delete code" in query:
            file = open("Generated_Code.txt", "w")
            file.write("")
            file.close()
            speak("Generated code deleted succesfully sir, do yu want me to do something else")

        elif "delete the code" in query:
            file = open("Generated_Code.txt", "w")
            file.write("")
            file.close()
            speak("Generated code deleted succesfully sir, do yu want me to do something else")

        elif "delete the generated code" in query:
            file = open("Generated_Code.txt", "w")
            file.write("")
            file.close()
            speak("Generated code deleted succesfully sir, do yu want me to do something else")

        elif 'search on YouTube' in query:
            speak("What Should I search on youtube sir")
            yts = Listenme()
            speak("Searching For your query sir")
            webbrowser.open("https://www.youtube.com/results?search_query=" + yts)
            time.sleep(3)
            speak("This is what I found sir")

        elif 'play on YouTube' in query:
            speak("What Should I play on youtube sir")
            yts = Listenme()
            speak("Searching For your query sir")
            pywhatkit.playonyt(yts)
            time.sleep(5)
            speak("May this help you sir")


        elif 'search on google' in query:
            import wikipedia as googleScrap

            speak("What Should I search on google sir")
            gts = Listenme()
            speak("Searching for your query sir")
            try:
                pywhatkit.search(gts)
                result = googleScrap.summary(gts, 2)
                speak(result)
                print(result)
            except:
                speak("Please take a look sir because there is no speakable data is present")

        elif 'search on Google' in query:
            import wikipedia as googleScrap

            speak("What Should I search on google sir")
            gts = Listenme()
            speak("Searching for your query sir")
            try:
                pywhatkit.search(gts)
                result = googleScrap.summary(gts, 2)
                speak(result)
                print(result)
            except:
                speak("Please take a look sir because there is no speakable data is present")
        elif 'break' in query:
            speak('ok sir, call me any time')
            speak('just say wake up Surya')
            break

        elif 'sleep' in query:
            speak('ok sir, call me any time')
            speak('just say wake up Surya')
            break

        elif 'factorial' in query:
            speak("Which number factorial you want to find sir")
            speak("Please input the number sir")
            g = int(input("Please input the number here:-"))
            f = int(g)
            fa = 1
            if f < 0:
                speak("Factorial of this does not exist sir")
                print("Factorial of this does not exist sir")
            elif f == 0:
                speak("sir,the factorial of 0 is 1")
                print("Factorial of 0 is 1")
            else:
                for i in range(1, f + 1):
                    fa = fa * i
                print("The Factorial of", g, "is", fa)
                speak(f"the factorial of {g} is {fa} sir")

        elif 'shut down' in query:
            speak("Do you really want to shutdown this computer sir")
            shut = Listenme()
            if "yes" in shut:
                speak("Shutting down your computer sir")
                os.system("shutdown /s /t 1")
            elif "no" in shut:
                speak("Ok sir I am not shutting down your computer")
            else:
                speak("No command given sir so I am not shutting down your computer")

        elif 'handwriting' in query:
            speak("speak the sentence sir")
            handtext = Listenme()
            pywhatkit.text_to_handwriting(handtext)
            speak("Your handwriting is generated sir")


        elif "reminder" in query:
            remindme()


        elif "pause" in query:
            speak("pausing currently playing media sir")
            play()

        elif query == "play":
            speak("paused Media Played sir")
            play()

        elif "next track" in query:
            play()
            speak("Playing Next Track Sir")
            next_track()


        elif "previous track" in query:
            play()
            speak("Playing Previous Track Sir")
            previous_track()
        elif "next song" in query:
            play()
            speak("Playing Next Track Sir")
            next_track()


        elif "previous song" in query:
            play()
            speak("Playing Previous Track Sir")
            previous_track()
        elif "last song" in query:
            play()
            speak("Playing Previous Track Sir")
            previous_track()
        elif "last track" in query:
            play()
            speak("Playing Previous Track Sir")
            previous_track()

        elif "increase the volume" in query:
            numbers = []
            current_number = ""
            for char in query:
                if char.isnumeric():
                    current_number += char
                else:
                    if current_number:
                        numbers.append(int(current_number))
                        current_number = ""
            if current_number:
                numbers.append(int(current_number))
            num = int(current_number) // 2
            for i in range(0, num):
                time.sleep(0.3)
                increase_volume()
            speak(f"volume increased by {current_number}")


        elif "decrease the volume" in query:
            numbers = []
            current_number = ""
            for char in query:
                if char.isnumeric():
                    current_number += char
                else:
                    if current_number:
                        numbers.append(int(current_number))
                        current_number = ""
            if current_number:
                numbers.append(int(current_number))
            num = int(current_number) // 2
            for i in range(0, num):
                time.sleep(0.3)
                decrease_volume()
            speak(f"volume decreased by {current_number}")

        elif "read the window" in query:
            speak("Window Reading initiated sir")
            Take_Shot()
            con = ocr_extracter()
            speak(f"The content written in the window is {con}")
            os.remove("Reader.png")

        elif "read the content" in query:
            speak("Window Reading initiated sir")
            Take_Shot()
            con = ocr_extracter()
            speak(f"The content written in the window is {con}")
            os.remove("Reader.png")

        elif "read content" in query:
            speak("Window Reading initiated sir")
            Take_Shot()
            con = ocr_extracter()
            speak(f"The content written in the window is {con}")
            os.remove("Reader.png")

        elif "read window" in query:
            speak("Window Reading initiated sir")
            Take_Shot()
            con = ocr_extracter()
            speak(f"The content written in the window is {con}")
            os.remove("Reader.png")

        else:
            pass