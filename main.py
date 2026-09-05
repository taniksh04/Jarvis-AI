import speech_recognition as sr
import webbrowser
import pyttsx4
import musicLibrary
import requests
import os
from google import genai
import asyncio
import edge_tts
import tempfile
from dotenv import load_dotenv

# Suppress Pygame's support prompt before importing Pygame.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# Load variables from .env file
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not NEWS_API_KEY or not GEMINI_API_KEY:
    raise RuntimeError("NEWS_API_KEY and GEMINI_API_KEY must be set in .env")

# Initialize Clients
r = sr.Recognizer()
google_client = genai.Client(api_key=GEMINI_API_KEY)

# Offline fallback for when Edge TTS or audio playback is unavailable.
def speak_old(text):
    engine = pyttsx4.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    
# Helper function to play MP3 files safely via Pygame
async def speak_async(text: str, voice: str = "en-US-ChristopherNeural"):

    """Generates audio using Edge TTS and plays it using pygame."""
    file_descriptor, file_path = tempfile.mkstemp(suffix=".mp3")
    os.close(file_descriptor)

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(file_path)

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        if os.path.exists(file_path):
            os.remove(file_path)

# Speak Function for edgetts
def speak(text: str):
    """Use Edge TTS first, then fall back to offline pyttsx4."""
    if not text or not text.strip():
        return

    try:
        asyncio.run(speak_async(text))
    except Exception as edge_error:
        print(f"Edge TTS failed; using offline voice: {edge_error}")
        try:
            speak_old(text)
        except Exception as fallback_error:
            print(f"Offline voice failed: {fallback_error}")

# Gemini Processing the command
def AIprocess(prompt):
    """Sends prompt to Gemini with system instructions to stay concise."""
    chat = google_client.chats.create(
        model='gemini-3.5-flash-lite',
        config={
            'system_instruction': (
                'You are Jarvis, a highly intelligent and polite AI assistant. '
                'Keep all answers to 1-2 short sentences so they sound natural when spoken.')})
    response = chat.send_message(prompt)
    return response.text

# Process the Command in different ways
def processCommand(c):
    command = c.strip().lower()

    # Open Various Websites
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "open gmail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://gmail.com")
    elif "open news" in command:
        speak("Opening Hindustan Times News Webpage ")
        webbrowser.open("https://www.hindustantimes.com")
    elif "open code wars" in command:
        speak("Opening Codewars")
        webbrowser.open("https://www.codewars.com")
    elif "open github" in command:
        speak("Opening Github")
        webbrowser.open("https://www.github.com")
    
    # Play Music from musicLibrary
    elif command.startswith("play"):
        # maxsplit=1 splits only on the first space after 'play'
        song = command.removeprefix("play").strip()
        link = next(
            (link for name, link in musicLibrary.music.items()
             if name.lower() == song),
            None,
        )
        if link:
            webbrowser.open(link)
        elif song:
            speak(f"Song '{song}' not found in music library.")
        else:
            speak("Please tell me which song to play.")

    # Speak NEWS HEADLINES from NEWS_API
    elif "what is the news" in command:
        response = requests.get(f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])[:3]

            # Speak the Top 3 Headlines
            speak("Here are top headlines.")
            for article in articles:
                speak(article["title"])
        else:
            speak("Unable to fetch news at the moment.")

    # Let GoogleAI handle the request
    else:
        output = AIprocess(c)
        speak(output)

# Main Functioning of Jarvis
if __name__ == "__main__":

    # Starting Jarvis
    speak("Voice systems initialized. Jarvis online.")

    # Calibrate the microphone once
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=1)

        # Keep the calibrated threshold stable during the long-running loop.
        r.dynamic_energy_threshold = False
        print(f"Microphone ready (energy threshold: {r.energy_threshold:.0f})")
    
    # Getting Jarvis Ready for Commands
    while True:

        # Start recognizing
        print("recognizing...")
        try:
            # obtain audio from the microphone
            with sr.Microphone() as source:
                # Listen the sound input
                print("Listening...")
                audio = r.listen(source,timeout=3, phrase_time_limit=5)

            # recognize speech using Google Speech Recognition
            word = r.recognize_google(audio, language="en-US")

            # Listen for the wake word 'Jarvis'
            if("jarvis" in word.lower()):
                speak("Yaa")
                    
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, phrase_time_limit=7)                        
                    command = r.recognize_google(audio)

                # Process the Command                
                processCommand(command)
        # Error for Unknown Value or Timeout
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            continue # Silence during listening timeout, continue loop
        # Error for Requests 
        except sr.RequestError as error:
            print(f"Speech Recognition network error: {error}")
            print("Check your internet connection, firewall, proxy, or Google Speech service.")
        # Any Other Errors    
        except Exception as e:
            print(f"Unexpected listening error: {type(e).__name__}: {e}")
