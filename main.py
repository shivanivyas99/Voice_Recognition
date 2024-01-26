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



# Define your ENABLE_LOGS and ENABLE_SPEECH_RESPONSES variables
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
    """
    Logs the input value.

    Parameters:
    value (str): The value to be logged.
    read_aloud (bool, optional): If True, the value is also read aloud. Defaults to False.

    Returns:
    None

    This function prints the input value if logging is enabled. 
    If read_aloud is True, it also converts the value to speech.
    """
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
    """
    Captures and recognizes audio from the user using Google's speech recognition API.

    This function allows multiple audio inputs from the user. It logs the start of each input and the result of the recognition. 
    In case of an error, it logs the error and adds a default error message to the recognized texts.
    """
    global recognized_texts
    r = sr.Recognizer()

    log("Record commands", True)

    for i in range(2):  # Allowing 2 inputs
        with sr.Microphone() as source:
            log(f"Start Speaking ({i+1} of 2):")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            recognized_texts.append(text)
            log("Audio captured.", True)
        except Exception as e:
            log("Error: " + str(e))
            recognized_texts.append("Error in recognizing audio.")

def get_recognized_text():
    """
    Returns the recognized texts.
    """
    if recognized_texts:
        return "\n".join(f"{i + 1}. {text.capitalize()}" for i, text in enumerate(recognized_texts))
    else:
        return "No audio input was recognized."

def display():
    """
    Asks the user if they want to see the recognized text.
    """
    view_text = input("Do you want to see the recognized text? (y/n): ")
    if view_text.lower() == 'y':
        log("Recognized text is given below:")
        log(get_recognized_text())
    else:
        log("See you soon!", True)
    log("Success!", True)

if __name__ == "__main__":
    init()
    request_current_status()
    communication()
    display()
