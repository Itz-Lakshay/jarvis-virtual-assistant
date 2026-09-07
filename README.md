# Jarvis – Voice Virtual Assistant

Jarvis is a Python-based voice assistant, inspired by tools like Alexa and Google Assistant. It listens for a wake word ("Jarvis"), then executes voice commands — opening websites, playing music, reading the time/date and news headlines, and falling back to an AI chat model for general questions.

## Features

- **Wake-word activation** – continuously listens in the background and only starts processing commands after hearing "Jarvis"
- **Website shortcuts** – opens Google, YouTube, LinkedIn, and Facebook on request
- **Music playback** – plays songs from a local music library (`musicLibrary.py`)
- **Time & date** – speaks the current time or date
- **News headlines** – fetches and reads out top headlines via the NewsAPI
- **AI conversation fallback** – any command that doesn't match a built-in action is sent to an OpenAI chat model, with conversation history maintained (and trimmed) across turns
- **Text-to-speech** – uses gTTS + pygame for natural-sounding speech, with a `pyttsx3`-based offline fallback
- **Logging** – all commands and actions are logged to `jarvis.log` for debugging/history

## Tech Stack

- **Python 3**
- `speech_recognition` – voice input / wake-word and command capture
- `gTTS` + `pygame` – text-to-speech playback
- `pyttsx3` – offline TTS fallback
- `openai` – AI chat responses (GPT-3.5-turbo)
- `requests` – NewsAPI integration
- `python-dotenv` – environment variable management for API keys

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_key_here
   NEWS_API_KEY=your_newsapi_key_here
   ```
3. Run the assistant:
   ```bash
   python main.py
   ```
4. Say "Jarvis" to activate, then speak a command.

## Example Commands

- "Open YouTube"
- "Play [song name]"
- "What's the time?"
- "What's today's date?"
- "Give me the news"
- Anything else gets routed to the AI assistant for a conversational response

## What I Learned

- Handling real-time audio input and speech recognition with the `speech_recognition` library
- Managing API keys securely using environment variables instead of hardcoding them
- Maintaining and trimming conversation history so an LLM-based chat feature doesn't grow unbounded
- Structuring a command-based dispatch system (`processCommand`) to route input to the right handler
- Adding logging to make a voice-driven app easier to debug, since you can't always "see" what it's doing

## What I'd Improve With More Time

- More reliable wake-word detection (current approach re-listens on a timeout loop, which can miss or mis-trigger)
- A simple GUI or system tray indicator to show listening/active state
- Expanding the music library and command set (e.g. weather, reminders, smart-home style commands)
- Better error handling/user feedback when speech recognition fails or misunderstands a command
- Packaging it so it can run as a background service instead of a terminal script

## Project Status

Functional prototype — core voice command loop, TTS, and AI fallback all work end-to-end. Submitted as part of the ACE "Build Something" task.