import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import random

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# random song URLs
song_library = [
    "https://www.youtube.com/watch?v=STUt9ueTnVU&list=PL0No2_vAYurOUv9mM4ea6-G9iJcukxKF3&index=6",
    "https://www.youtube.com/watch?v=yznQfliI65s&list=PL0No2_vAYurOUv9mM4ea6-G9iJcukxKF3&index=1",
    "https://www.youtube.com/watch?v=APc4tGae9dg&list=PL0No2_vAYurOUv9mM4ea6-G9iJcukxKF3&index=26",
    # Add more songs as needed
]

# Predefined conversation
conversational_responses = {
    "how are you": "I'm just a computer program, so I don't have feelings, but thanks for asking!",
    "what is your name": "I'm Alfred, your personal assistant.",
    "who created you": "I was created by a developer named Ayush, using various programming tools.",
    "what can you do": "I can open websites, tell jokes, play music, give you the weather, and more. How can I assist you today?",
    "tell me about yourself": "I'm Alfred, your virtual assistant. I'm here to help you with various tasks and provide information.",
    "thank you": "No need to thank me. How can I assist you further?",
    "can You Sing": "I'm a virtual assistant, not a pop star!",
    "why is your name Alfred": "Ask my developer.",
    "can you do math": "No, maybe in the next update I could.",
    "do you have a girlfriend?": "I'm a virtual assistant, so my only relationship is with data! But if I did have a girlfriend, she'd probably be a super-fast processor with a great sense of humor."
}

# weather updates
def get_weather():
    try:
        response = requests.get("http://wttr.in/?format=%C+%t")
        if response.status_code == 200:
            weather_report = response.text.strip()
            speak(f"The current weather is: {weather_report}")
        else:
            speak("I couldn't retrieve the weather information.")
    except requests.RequestException as e:
        speak(f"Error fetching weather: {str(e)}")

#  headlines
def get_news():
    try:
        api_key = "_"  # Replace with your free NewsAPI key
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json()["articles"]
            headlines = [article["title"] for article in articles[:5]]
            news_report = "Here are the top news headlines: " + ". ".join(headlines)
            speak(news_report)
        else:
            speak("I couldn't retrieve the news headlines.")
    except requests.RequestException as e:
        speak(f"Error fetching news: {str(e)}")

# to tell a joke
def tell_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke = response.json()
            joke_text = f"Here's a joke: {joke['setup']}... {joke['punchline']}"
            speak(joke_text)
        else:
            speak("I couldn't retrieve a joke at this time.")
    except requests.RequestException as e:
        speak(f"Error fetching joke: {str(e)}")

#  to play a random song
def play_random_song():
    try:
        song_url = random.choice(song_library)
        webbrowser.open(song_url)
        speak("Playing a random song for you")
    except Exception as e:
        speak(f"Error playing song: {str(e)}")

def process_command(command):
    try:
        command = command.lower()

        if any(word in command for word in ["stop", "exit", "quit"]):
            speak("Have a good day!")
            return False

        for key in conversational_responses:
            if key in command:
                speak(conversational_responses[key])
                return True

        if "open google" in command:
            webbrowser.open("https://google.com")
            speak("Opening Google")
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        elif "open linkedin" in command:
            webbrowser.open("https://linkedin.com")
            speak("Opening LinkedIn")
        elif "open facebook" in command:
            webbrowser.open("https://facebook.com")
            speak("Opening Facebook")
        elif "open twitter" in command:
            webbrowser.open("https://twitter.com")
            speak("Opening Twitter")
        elif "open reddit" in command:
            webbrowser.open("https://reddit.com")
            speak("Opening Reddit")
        elif "weather" in command:
            get_weather()
        elif "news" in command:
            get_news()
        elif "joke" in command:
            tell_joke()
        elif "play a song" in command or "play music" in command or "song" in command or "music" in command :
            play_random_song()
        else:
            speak("Sorry, I didn't understand that command")
        return True
    except Exception as e:
        speak(f"Error processing command: {str(e)}")
        return True

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        speak(f"Error listening: {str(e)}")
        return None

if __name__ == "__main__":
    speak("Good morning sir")
    speak("How can I assist you today")

    while True:
        try:
            command = listen()
            if command:
                print(f"Command received: {command}")
                if not process_command(command):
                    break

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except Exception as e:
            print(f"Error: {e}")
