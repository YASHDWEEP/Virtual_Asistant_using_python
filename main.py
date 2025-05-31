import speech_recognition as sr  # Recognizes speech from the microphone.
import webbrowser  # Opens web URLs in a browser.
import pyttsx3 as pt  # Used for text-to-speech functionality.
import musicLibrary  # Used for music library functionality.
import requests  # Used for web requests.


recognizer = sr.Recognizer()  # Recognizer object to recognize speech.
engine = pt.init()  # instialization of pytttsx3
news = "27f8c3e89b254e3da652430aa9296727"  # API key for news API.


# speak function to convert text to speech
def speak(text):
    engine.say(text)  # converts text to speech
    engine.runAndWait()  # waits for the speech to be completed


# Function for proccesing all the requests
def process_command(command):
    if command.lower() == "open google":
        webbrowser.open("https://www.google.com")
    elif command.lower() == "open youtube":
        webbrowser.open("https://www.youtube.com")
    elif command.lower() == "open facebook":
        webbrowser.open("https://www.facebook.com")
    elif command.lower() == "open linked in":
        webbrowser.open("https://www.linkedin.com")
    elif command.lower().startswith("play"):  # accesing the music library
        try:
            song = command.lower().split(" ")[
                1
            ]  # accesing song name by using the split function . split(" ") splits the string into a list of words and we accesss the 1st index word to get the song name
            link = musicLibrary.music[song]
            if link:
                webbrowser.open(link)
            else:
                speak(f"{song} is not available in the music library")
        finally:
            print("the Working of song Will be done.... ")
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
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news}"  # API URL for US news
        try:
            r = requests.get(url)  # Send a GET request to the API
            if r.status_code == 200:  # Check if the request was successful
                data = r.json()  # data can be  accessed using th json file
                articles = data.get(
                    "articles", []
                )  # articles is a list of dictionaries where each dictionary represents an article
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

    #  both the two exit statements are used to exit the program  I will write both logic only for my understanding
    elif command.lower() in [
        "exit",
        "stop",
        "shutdown",
    ]:  # Exit Assistant from the loop by uisng the exit function
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
    while running: # Continuously listen for user commands
        r = sr.Recognizer() # Create a Recognizer object
        print("Recongnizing......") 
        try: 
            with sr.Microphone() as source: # Use the default microphone as the audio source
                print("Listening..............................")
                audio = r.listen(source, timeout=6, phrase_time_limit=5) # Listen for 6 seconds and 5 seconds for a phrase
 
                word = r.recognize_google(audio) # Recognize the speech using Google Speech Recognition API
                print("You said : " + word) 
                if word.lower() == "jarvis":  
                    speak("yes how can I help you! ")
                    print("yes how can I help you! ")
                    with sr.Microphone() as source: # Use the default microphone as the audio source
                        print("  jarvis Activated ......") 
                        audio = r.listen(source, timeout=4)  # Listen for 4 seconds
                        command = r.recognize_google(audio) 
                        print("You said : " + command)
                        process_command(command) # Process the user's command

        except sr.UnknownValueError: # If the speech recognition API is unable to recognize the speech
            print("jarvis Could not understand what you said") # Print an error message
        except Exception as e:
            print("Error : ", e)
