import pyttsx3
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import subprocess
import time
import requests
import json
import cv2

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  

    speak('I am Pops')
    speak('Please tell me how may I help you')       


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        speak('Your voice is recognizing')    
        query = r.recognize_google(audio, language='en-IN')
        print('User said:', query)
        
    except Exception as e:
        print("Your voice is not received. Say that again, please...")
        speak('Your voice is not received.')
        speak('Say that again, please...')  
        return "None"

    return query


def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["cod"] == "404":
            speak("City not found!")
        else:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            speak(f"Weather in {city}: {weather_desc}")
            speak(f"Temperature: {temp} degrees Celsius")
            speak(f"Humidity: {humidity}%")
            speak(f"Wind Speed: {wind_speed} km/h")

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't fetch the weather information.")


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com/")

        elif 'open stackoverflow' in query:
            webbrowser.open("https://www.stackoverflow.com/")

        elif "camera" in query or "take a photo" in query:
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()
            if ret:
                cv2.imwrite("img.jpg", frame)
                speak("Photo captured successfully!")
                camera.release()
            else:
                speak("Sorry, I couldn't capture the photo.")

        elif 'play music' in query:
            music_dir = "C:\\Users\\nivik\\3D Objects\\music"
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[1]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M%p")    
            speak(f'Current time is: {strTime}')

        elif 'the date' in query:
            date = datetime.date.today()
            speak(date)

        elif 'email to ' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "YourfriendEmail@gmail.com"    
                sendEmail=(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, my friend. I am not able to send this email")

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to locate")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location)

        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open('chrome://newtab/', query)

        elif "log off" in query or "sign out" in query:
            speak("Make sure all the applications are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", ""])

        elif 'quit' in query:
            speak("Goodbye sir, I am going to sleep!")
        break
