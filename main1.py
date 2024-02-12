import speech_recognition as sr
from openai import OpenAI
from pathlib import Path
import os
from dotenv import load_dotenv
from pygame import mixer

# Load the API key from an environment variable
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Defining ENABLE_LOGS and ENABLE_SPEECH_RESPONSES variables
ENABLE_LOGS = True
ENABLE_SPEECH_RESPONSES = True

def text_to_speech(input_text: str):
    """
    Converts the input text to speech using the OpenAI API.

    Parameters:
    input_text (str): The text to be converted to speech.

    Returns:
    None

    This function generates audio from the input text and saves it to a file.
    """
    speech_file_path = Path("output.mp3")
    try:
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=input_text
            #input="This function generates audio from the input text and saves it to a file."
        ) as response:
            response.stream_to_file(speech_file_path)
            
        mixer.music.load(speech_file_path)
        mixer.music.play()
        # Optionally, add code here to play the saved audio file
    except Exception as e:
        print(f"Error in text to speech conversion: {e}")

def log(value: str, read_aloud: bool = False):
    
    if ENABLE_LOGS:
        print(value)
    if ENABLE_SPEECH_RESPONSES and read_aloud:
        text_to_speech(value)

def init():
    """
    Initializes the system.
    """
    mixer.init()
    # log("Inside init()", True)

def request_current_status():
    """
    Requests the current status of the system.
    """
    # log("Request current status () == true")

# List to store recognized texts
recognized_texts = []

def communication():
    
    global recognized_texts
    r = sr.Recognizer()

    while True:  # Loop until the user confirms
        with sr.Microphone() as source:
            log("Please start speaking...", True)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            log(f"Did you say: '{text}'?", True)

            # Ask for confirmation using voice
            log("Did I get that right? Please say yes or no.", True)
            with sr.Microphone() as source:
                confirmation_audio = r.listen(source)
            confirmation_response = r.recognize_google(confirmation_audio).lower()

            if "yes" in confirmation_response:
                recognized_texts.append(text)
                log("That is perfect, see you soon!", True)
                break  # Exit loop if confirmed
            elif "no" in confirmation_response:
                log("Let's try again. Please speak again.", True)
            else:
                log("I didn't understand. Please say yes or no.", True)
        except sr.UnknownValueError:
            log("I didn't catch that. Let's try again.", True)
        except Exception as e:
            log(f"Error: {e}")


def get_recognized_text():
    """
    Returns the recognized texts.
    """
    if recognized_texts:
        return "\n".join(f"{i + 1}. {text.capitalize()}" for i, text in enumerate(recognized_texts))
    else:
        return "No audio input was recognized."

def display():
    
    if recognized_texts:
        for text in recognized_texts:
            log(f"Recognized: {text}", True)
    else:
        log("No audio input was recognized.", True)


if __name__ == "__main__":
    init()
    request_current_status()
    communication()
    display()
