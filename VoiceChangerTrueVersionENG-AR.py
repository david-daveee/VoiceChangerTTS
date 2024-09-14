import speech_recognition as sr
from gtts import gTTS
import os
import threading
import pygame
import time
import glob

#Code for check indexes
#import sounddevice as sd
#print(sd.query_devices())

# Indexes for HyperX microphone and VB-Audio output
MIC_DEVICE_INDEX = 2  # Index of your microphone (HyperX QuadCast S)
OUTPUT_DEVICE_INDEX = 28  # VB-Audio Index (CABLE Input)


# Function to delete old entries
def delete_old_records():
    files = glob.glob("speech_*.mp3")
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Failed to delete {f}: {e}")


def speak_text(text):
    # Deleting old entries before creating a new one
    delete_old_records()

    # Create a unique filename based on time
    filename = f"speech_{int(time.time())}.mp3"

    # Translate text and voice it in Arabic
    tts = gTTS(text=text, lang="ar")
    tts.save(filename)  # Save the file in the current directory

    # Initialize pygame to play on default device
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue  # Waiting for playback to complete

    pygame.mixer.quit()  # Explicitly shutdown the mixer before deleting the file
    os.remove(filename)  # Delete the file after use is complete


def continuous_listen_and_talk():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
        print("Setting up noise reduction...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Increased time for noise reduction
        print("I'm starting to listen...")

        while True:
            try:
                print("I'm listening...")

                # Recognize speech in English
                audio = recognizer.listen(source, timeout=0, phrase_time_limit=5)
                print("Processing...")
                text = recognizer.recognize_google(audio, language="en-US")  # English language
                print(f"You said: {text}")

                # Start voice-over in Arabic in a separate thread
                thread = threading.Thread(target=speak_text, args=(text,))
                thread.start()

            except sr.UnknownValueError:
                print("Speech recognition failed, please try again...")
            except sr.RequestError as e:
                print(f"Speech recognition service error; {e}")
            except sr.WaitTimeoutError:
                print("The microphone is silent, I continue to listen...")


if __name__ == "__main__":
    continuous_listen_and_talk()
