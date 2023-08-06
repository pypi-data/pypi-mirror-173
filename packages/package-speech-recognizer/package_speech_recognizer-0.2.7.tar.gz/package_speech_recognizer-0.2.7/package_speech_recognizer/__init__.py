'''
Aim: (1) To keep background listning on
     (2) On wake word respond
'''

from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError, WaitTimeoutError
import pyttsx3
import playsound


def speak(text, voice_id=1, rate=170, volume=1):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    text = str(text)
    engine.say(text)
    engine.runAndWait()

def background_listner(language = "en-us"):
    recognizer = Recognizer()
    with Microphone() as microphone:
        print("Background_listning...")
        audio_data = recognizer.listen(microphone, 5, 5)
        voice_data = ""
        try:
            voice_data = recognizer.recognize_google(audio_data, language=language)
        except UnknownValueError: 
            print("I Didn't get that")
        except RequestError:
            print('Sorry, the service is down')
        except WaitTimeoutError:
            print("what the actual fucking problem is this")
        print("you: ", voice_data.lower())
        return voice_data.lower()

def main_listner(language = "en-In"):
    recognizer = Recognizer()
    with Microphone() as microphone:
        print("Main_listning...")
        audio_data = recognizer.listen(microphone, 5, 5)
        voice_data = ""
        try:
            voice_data = recognizer.recognize_google(audio_data, language=language)
        except UnknownValueError: 
            print("I Didn't get that")
        except RequestError:
            print('Sorry, the service is down')
        except WaitTimeoutError:
            print("what the actual fucking problem is this")
        print("you: ", voice_data.lower())
        return voice_data.lower()

def wake_word_detector(word, wake_words):
    for i in range(len(wake_words)):
        if wake_words[i]==word:
            return True 

def full_speech_controller(voice_data, func, sow=None,wake_words= ["this","is", "an", "example", "recommnded", "to", "use", "your", "dataset"], language = "en-In"):
    detector = wake_word_detector(voice_data, wake_words)
    if detector:
        print("wake word detected: ", voice_data)
        if sow is not None:
            playsound.playsound(sow)
        listner = main_listner(language=language)
        func(listner)


