import speech_recognition as sr

recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except sr.UnknownValueError:

        print("Could not understand audio")

        return ""

    except sr.RequestError:

        print("Speech recognition service unavailable")

        return ""