import speech_recognition as sr

import time

recognizer = sr.Recognizer()
consecutive_failures = 0
is_degraded = False

def listen(timeout=5):
    global consecutive_failures, is_degraded

    if is_degraded:
        # Prevent rapid polling when service is down
        time.sleep(2)
        
    try:
        # print("Microphone Status: Initializing...")
        with sr.Microphone() as source:
            status = "Degraded" if is_degraded else "Active"
            print(f"Listening Status: {status}")
            
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                return ""
                
    except OSError as e:
        print(f"Microphone Error (Missing or Disconnected): {e}")
        time.sleep(2)
        return ""
    except Exception as e:
        print(f"Unexpected Microphone Error: {e}")
        time.sleep(2)
        return ""

    try:
        text = recognizer.recognize_google(audio)
        
        # Reset recovery metrics on success
        consecutive_failures = 0
        if is_degraded:
            is_degraded = False
            print("[Voice Service Restored]")
            
        print("You said:", text)
        return text.lower()

    except sr.UnknownValueError:
        # Mumbled speech is normal, not a system failure
        print("Could not understand audio")
        return ""

    except sr.RequestError as e:
        consecutive_failures += 1
        print(f"Speech recognition service unavailable. Recovery Attempts: {consecutive_failures}/3")
        
        if consecutive_failures >= 3 and not is_degraded:
            is_degraded = True
            print("[Voice Service Degraded] RohitOS continues running.")
            
        time.sleep(2)
        return ""
    except Exception as e:
        print(f"Unexpected Recognition Error: {e}")
        time.sleep(2)
        return ""