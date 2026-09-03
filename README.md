# Jarvis AI Assistant

Jarvis is a Python voice assistant that listens for the wake word `Jarvis`, opens websites, plays music links, reads news headlines, and uses Gemini for general questions.

## Features

- Voice input through SpeechRecognition
- Wake-word detection using `Jarvis`
- Gemini AI responses
- News headlines through NewsAPI
- Website and music commands
- Microsoft Edge TTS for natural speech
- Offline `pyttsx4` fallback when Edge TTS or audio playback fails

## Requirements

- Windows
- Python 3.12 or compatible Python version
- A working microphone and speakers
- Internet access for Google Speech Recognition, Gemini, NewsAPI, and Edge TTS
- API Keys of Google AI Studios and NewsAPI

## Setup

1. Clone the repository and open its folder:

   ```powershell
   git clone https://github.com/taniksh04/Jarvis-AI.git
   cd Jarvis-AI
   ```

2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Create your environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Open `.env` and add your own API keys:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   NEWS_API_KEY=your_news_api_key
   ```

6. Start Jarvis:

   ```powershell
   python main.py
   ```

## Example Commands

After hearing the wake word, try:

- `Open Google`
- `Open YouTube`
- `Open Gmail`
- `Open news`
- `Play Superman`
- `Tell news`
- Ask a general question

## TTS Fallback

Jarvis tries Edge TTS first because it provides natural online voices. If Edge TTS or Pygame audio playback fails, the application automatically uses offline `pyttsx4` speech instead.

Here are some different voices provided by Edge TTS. You can Use them according to your convenience. Just change "en-US-ChristopherNeural" this with any of 
the voice codes.
("en-US-ChristopherNeural"-Male-US-Deep,authoritative)("en-US-GuyNeural"-Male-US-Conversational,natural) 
("en-US-JennyNeural"-Female-US-Friendly,professional)("en-GB-RyanNeural"-Male-UK-Sophisticated British)
("en-GB-SoniaNeural"-Female-UK-Clear British accent)("en-IN-PrabhatNeural"-Male-India-Expressive Indian accent)

Temporary audio files are removed after playback, including when an error occurs.

## Security

Never commit `.env` or expose API keys in source code. The repository ignores `.env`; only `.env.example` should be committed. Use your own API keys when running this project.

## Project Files

- `main.py`: Assistant logic, speech recognition, TTS, Gemini, news, and commands
- `musicLibrary.py`: Music name and URL mappings
- `requirements.txt`: Python dependencies
- `.env.example`: Safe environment-variable template
- `.gitignore`: Files excluded from Git
