import speech_recognition as sr
from core.runtime_states import print_ux_state

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
            state_str = "Listening (Degraded)" if is_degraded else "Listening"
            print_ux_state(state_str)
            
            # Calibration and threshold adjustments for better capture
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recognizer.pause_threshold = 1.5
            recognizer.non_speaking_duration = 0.5
            
            try:
                # Increased phrase_time_limit so sentences aren't cut off midway
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
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
            
        audio_duration = len(audio.frame_data) / (audio.sample_rate * audio.sample_width)
        print("You said:", text)
        print(f"Words Captured: {len(text.split())}")
        print(f"Recognition Length: {len(text)} chars")
        print(f"Audio Duration: {audio_duration:.2f}s")
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