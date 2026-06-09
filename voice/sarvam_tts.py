# voice/sarvam_tts.py
# Handles text-to-speech output using Sarvam AI

import os
import base64
import requests
import subprocess

def speak(text):
    """
    Speaks the text using Sarvam AI TTS.
    Raises Exception on any failure so the router can fallback.
    """
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        raise Exception("SARVAM_API_KEY not found in environment.")
        
    valid_speakers = ["priya", "simran", "shreya", "rahul", "aditya", "ritu", "ashutosh", "neha", "pooja", "rohan", "kavya", "amit", "dev", "ishita", "ratan", "varun", "manan", "sumit", "roopa", "kabir", "aayan", "shubh", "advait", "anand", "tanya", "tarun", "sunny", "mani", "gokul", "vijay", "shruti", "suhani", "mohit", "kavitha", "rehan", "soham", "rupali", "niharika"]
    speaker = os.getenv("SARVAM_SPEAKER", "rahul").lower()
    if speaker not in valid_speakers:
        speaker = "rahul"

    print(f"[Sarvam Voice]\nSpeaker: {speaker}")

    url = "https://api.sarvam.ai/text-to-speech"
    payload = {
        "inputs": [text],
        "target_language_code": "hi-IN",
        "speaker": speaker,
        "model": "bulbul:v3",
        "speech_sample_rate": 16000,
        "enable_preprocessing": True,
        "pace": 1.1
    }
    headers = {
        "api-subscription-key": api_key,
        "Content-Type": "application/json"
    }

    print("[TTS] Calling Sarvam AI...")
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    
    if response.status_code != 200:
        raise Exception(f"Sarvam API failed: {response.status_code} {response.text}")
        
    data = response.json()
    if "audios" in data and len(data["audios"]) > 0:
        audio_base64 = data["audios"][0]
        audio_bytes = base64.b64decode(audio_base64)
        
        os.makedirs("data", exist_ok=True)
        wav_path = os.path.join("data", "temp_tts.wav")
        with open(wav_path, "wb") as f:
            f.write(audio_bytes)
            
        print(f"RohitOS says: {text}")
        print("[TTS Speaking - Sarvam]")
        # Play synchronously via PowerShell
        # Note: SoundPlayer requires an absolute path or relative from CWD, temp_tts.wav is in data/
        abs_wav_path = os.path.abspath(wav_path)
        subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{abs_wav_path}').PlaySync()"], check=True)
        print("[TTS Completed]")
    else:
        raise Exception("No audio returned from Sarvam API")
