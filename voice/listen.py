import speech_recognition as sr
from core.runtime_states import print_ux_state

import time

recognizer = sr.Recognizer()
consecutive_failures = 0
is_degraded = False

DIAGNOSTICS = False  # Set True for debugging only
DEBUG_STT = False  # Set True to show calibration threshold values

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
            
            # One-time calibration at startup (Option A)
            if not getattr(recognizer, 'is_calibrated', False):
                if DEBUG_STT:
                    print("\n[STT] Calibrating microphone... Please remain quiet for 1 second.")
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                raw_threshold = recognizer.energy_threshold
                clamped_threshold = max(150, min(3000, raw_threshold))
                recognizer.energy_threshold = clamped_threshold
                
                recognizer.dynamic_energy_threshold = False
                recognizer.is_calibrated = True
                if DEBUG_STT:
                    print(f"[STT] Calibration complete.")
                    print(f"      Raw threshold: {raw_threshold:.2f}")
                    print(f"      Adjusted threshold: {clamped_threshold:.2f}")
                
            recognizer.pause_threshold = 1.5
            recognizer.non_speaking_duration = 0.5
            
            try:
                # Increased phrase_time_limit so sentences aren't cut off midway
                if DIAGNOSTICS:
                    print("[DIAGNOSTICS] Waiting for audio start...")
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                if DIAGNOSTICS:
                    print("[DIAGNOSTICS] Audio capture ended!")
                    audio_dur = len(audio.frame_data) / (audio.sample_rate * audio.sample_width)
                    print(f"[DIAGNOSTICS] Captured audio duration: {audio_dur:.2f}s")
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