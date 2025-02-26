import os
import datetime

import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

TWILIO_SAMPLE_RATE = 8000  # Hz
LOGS_DIR = "conversation_logs"

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Generate a filename based on current date and time
log_filename = os.path.join(LOGS_DIR, f"conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def on_open(session_opened: aai.RealtimeSessionOpened):
    """Called when the connection has been established."""
    print("Session ID:", session_opened.session_id)
    # Log session start to file
    with open(log_filename, "a") as f:
        f.write(f"Session started: {datetime.datetime.now()}\n")
        f.write(f"Session ID: {session_opened.session_id}\n\n")


def on_data(transcript: aai.RealtimeTranscript):
    """Called when a new transcript has been received."""
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(transcript.text, end="\r\n")
        # Write final transcript to file
        with open(log_filename, "a") as f:
            f.write(f"{transcript.text}\n")
    else:
        print(transcript.text, end="\r")


def on_error(error: aai.RealtimeError):
    """Called when the connection has been closed."""
    print("An error occurred:", error)
    # Log error to file
    with open(log_filename, "a") as f:
        f.write(f"Error: {error}\n")


def on_close():
    """Called when the connection has been closed."""
    print("Closing Session")
    # Log session close to file
    with open(log_filename, "a") as f:
        f.write(f"\nSession closed: {datetime.datetime.now()}\n")


class TwilioTranscriber(aai.RealtimeTranscriber):
    def __init__(self):
        super().__init__(
            on_data=on_data,
            on_error=on_error,
            on_open=on_open,  # optional
            on_close=on_close,  # optional
            sample_rate=TWILIO_SAMPLE_RATE,
            encoding=aai.AudioEncoding.pcm_mulaw
        )
