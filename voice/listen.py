import speech_recognition as sr

recognizer = sr.Recognizer()


def listen(timeout=5):

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return ""

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