import speech_recognition as sr
import webbrowser
import pyttsx3 as pt
import musicLibrary
import requests


recognizer = sr.Recognizer()
engine = pt.init()  # instialization of pytttsx3
news = "27f8c3e89b254e3da652430aa9296727"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def process_command(command):
    if command.lower() == "open google":
        webbrowser.open("https://www.google.com")
    elif command.lower() == "open youtube":
        webbrowser.open("https://www.youtube.com")
    elif command.lower() == "open facebook":
        webbrowser.open("https://www.facebook.com")
    elif command.lower() == "open linked in":
        webbrowser.open("https://www.linkedin.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        if link:
            webbrowser.open(link)
        else:
            speak(f"{song} is not available in the music library")
    # elif "news" in command.lower():
    #     # webbrowser.open("https://www.bbc.co.uk/news")

    #    # r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=27f8c3e89b254e3da652430aa9296727")  # for us

    #     r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=27f8c3e89b254e3da652430aa9296727")   # for india
    #     if r.status_code == 200 :
    #         #parse the Json Response
    #         data = r.json()
    #         #Extract the  articles
    #         articles  = data.get('articles',[])
    #         #speak the headlines
    #         for article in  articles :
    #             speak(article['title'])
    elif "news" in command.lower():
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                if articles:
                    speak("Here are the top news headlines.")
                    for i, article in enumerate(
                        articles[:5]
                    ):  # Read only top 5 headlines
                        speak(f"Headline {i+1}: {article['title']}")
                else:
                    speak("Sorry, I couldn't find any news articles.")
            else:
                speak(f"Failed to fetch news. HTTP status code: {r.status_code}")
        except Exception as e:
            speak("An error occurred while trying to fetch news.")
            print("Error fetching news:", e)

        else:
            speak("Sorry, I couldn't fetch the news right now.")
    elif command.lower() in ["exit", "stop", "shutdown"]:
        speak("Shutting down Jarvis. Goodbye!")
        print("Shutting down Jarvis. Goodbye!")
        exit()  # Terminates the program
    else:
        if command.lower() in ["exit", "stop", "shutdown"]:
            speak("Shutting down Jarvis. Goodbye!")
        print("Shutting down Jarvis. Goodbye!")
        running = False


if __name__ == "__main__":
    speak("Initializing jarvis .....")
    # listen for the ewake wor for jarvis
    running = True
    while running:
        r = sr.Recognizer()
        print("Recongnizing......")
        try:
            with sr.Microphone() as source:
                print("Listening..............................")
                audio = r.listen(source, timeout=8, phrase_time_limit=5)

                word = r.recognize_google(audio)
                print("You said : " + word)
                if word.lower() == "jarvis":
                    speak("yes how can I help you! ")
                    print("yes how can I help you! ")
                with sr.Microphone() as source:
                    print("  jarvis Activated ......")
                    audio = r.listen(source, timeout=4)
                    command = r.recognize_google(audio)
                    print("You said : " + command)
                    process_command(command)

        except sr.UnknownValueError:
            print("jarvis Could not understand what you said")
        except Exception as e:
            print("Error : ", e)
