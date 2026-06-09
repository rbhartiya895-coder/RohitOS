# test_sarvam_voices.py
import os
import time
import base64
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

def test_speaker(speaker):
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        print("SARVAM_API_KEY not found in environment.")
        return

    text = f"Hello Boss. I am {speaker}."
    
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

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code != 200:
            # Print the error but don't crash, so the loop can continue
            print(f" -> Failed for {speaker}: {response.status_code} {response.text}")
            return
            
        data = response.json()
        if "audios" in data and len(data["audios"]) > 0:
            audio_bytes = base64.b64decode(data["audios"][0])
            wav_path = os.path.abspath("test_voice_loop.wav")
            with open(wav_path, "wb") as f:
                f.write(audio_bytes)
                
            subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{wav_path}').PlaySync()"], check=True)
            print(f" -> Success: {speaker} played perfectly.")
        else:
            print(f" -> No audio returned for {speaker}")
            
    except Exception as e:
        print(f" -> Error testing {speaker}: {e}")

if __name__ == "__main__":
    speakers = ["anushka", "priya", "simran", "shreya", "rahul", "aditya"]
    
    for s in speakers:
        print(f"\nTesting: {s}")
        test_speaker(s)
        time.sleep(3)
