# voice/whisper_stt.py
# Handles speech-to-text using local Faster-Whisper

import speech_recognition as sr
import time
import numpy as np
from core.runtime_states import print_ux_state

# Global model instance
whisper_model = None
WHISPER_MODEL_SIZE = "base.en"

consecutive_failures = 0
is_degraded = False
DIAGNOSTICS = False  # Set True for debugging only
DEBUG_STT = False  # Set True to show calibration threshold values
recognizer = sr.Recognizer()

def init_whisper():
    global whisper_model
    if whisper_model is None:
        print(f"[Whisper STT] Initializing {WHISPER_MODEL_SIZE} model (this may take a moment on first run)...")
        try:
            from faster_whisper import WhisperModel
            # Using CPU and int8 for maximum compatibility and reasonable speed
            whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")
            print("[Whisper STT] Model loaded successfully.")
        except Exception as e:
            raise Exception(f"Failed to initialize Whisper: {e}")

def get_whisper_model_info():
    return WHISPER_MODEL_SIZE if whisper_model is not None else "Not Loaded"

def listen(timeout=5):
    global consecutive_failures, is_degraded
    
    init_whisper()

    if is_degraded:
        # Prevent rapid polling when service is down
        time.sleep(2)
        
    try:
        with sr.Microphone() as source:
            status = "Degraded" if is_degraded else "Active"
            state_str = "Listening (Whisper - Degraded)" if is_degraded else "Listening (Whisper)"
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
        # Convert audio directly to numpy array
        # speech_recognition captures at 16000 Hz, 16-bit PCM
        audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
        audio_np = np.frombuffer(audio_data, np.int16).flatten().astype(np.float32) / 32768.0
        
        segments, info = whisper_model.transcribe(audio_np, beam_size=5)
        
        text = "".join([segment.text for segment in segments]).strip()
        
        if not text:
            return ""
            
        # Reset recovery metrics on success
        consecutive_failures = 0
        if is_degraded:
            is_degraded = False
            print("[Whisper Service Restored]")
            
        print(f"[Whisper STT] Language: '{info.language}' (Prob: {info.language_probability:.2f})")
        print("You said:", text)
        
        return text.lower()

    except Exception as e:
        consecutive_failures += 1
        print(f"Whisper STT unavailable. Error: {e}")
        
        if consecutive_failures >= 3 and not is_degraded:
            is_degraded = True
            print("[Whisper Service Degraded]")
            
        time.sleep(2)
        # Raise exception to trigger failover in voice_router
        raise Exception(f"Whisper transcription failed: {e}")
