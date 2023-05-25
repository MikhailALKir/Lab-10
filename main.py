import pyaudio
import Word as WORD
import pyttsx3
import speech_recognition as sr
import vosk
import json

actual_word = None

tts = pyttsx3.init()
rate = tts.getProperty('rate')
tts.setProperty('rate', rate - 40)
volume = tts.getProperty('volume')
tts.setProperty('volume', volume + 0.9)
voices = tts.getProperty('voices')
tts.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')

model = vosk.Model('vosk-model-small-en-us-0.15')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def say(text):
    print("Bot said: " + text + "\n")
    tts.say(text)
    tts.runAndWait()


def listen():
    while True:
        print("Listening...")
        data = stream.read(8000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            print("Analysing...")
            answer = json.loads(record.Result())['text']
            print("You said: " + str(answer))
            if "find" in answer:
                global actual_word
                actual_word = find(answer)
            elif "mean" in answer:
                say_meaning()
            elif "examp" in answer:
                say_example()
            elif "name" in answer:
                say_word()
            elif "exit" in answer:
                exit()
            else:
                say("No such command")


def if_word_is_none(func):
    def wrapper(*args, **kwargs):
        if actual_word is None:
            say("At first you need to choose your word")
        else:
            return func(*args, **kwargs)

    return wrapper


def find(text):
    text = text.replace("find", "")
    text = text.replace(" ", "")

    try:
        word = WORD.getResponse(text)
        say(word.name)

        return word
    except:
        say("Can't find this word")
        return None


@if_word_is_none
def say_meaning():
    say(actual_word.meaning)


@if_word_is_none
def say_example():
    say(actual_word.example)


@if_word_is_none
def say_word():
    print(actual_word.phonetic)
    say(actual_word.name)


if __name__ == "__main__":

    while True:
        listen()
