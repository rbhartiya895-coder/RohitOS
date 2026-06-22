import os
import ctypes

try:
    from pycaw.pycaw import AudioUtilities
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False
    print("Warning: pycaw not installed. Volume mute will use fallback.")

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def _press_key(hexKeyCode):
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, 0, 0)
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, 2, 0)

def lock_computer():
    os.system('rundll32.exe user32.dll,LockWorkStation')
    return "Computer locked successfully."

def sleep_computer():
    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    return "Going to sleep mode."

def restart_computer():
    os.system('shutdown /r /t 1')
    return "Restarting computer."

def shutdown_computer():
    os.system('shutdown /s /t 1')
    return "Shutting down computer."

def volume_up():
    for _ in range(5):
        _press_key(VK_VOLUME_UP)
    return "Volume increased."

def volume_down():
    for _ in range(5):
        _press_key(VK_VOLUME_DOWN)
    return "Volume decreased."

def get_audio_volume():
    if not PYCAW_AVAILABLE:
        return None
    try:
        devices = AudioUtilities.GetSpeakers()
        return devices.EndpointVolume
    except Exception as e:
        print(f"Pycaw error: {e}")
        return None

def mute():
    vol = get_audio_volume()
    if vol:
        vol.SetMute(1, None)
    else:
        _press_key(VK_VOLUME_MUTE) # Fallback
    return "System audio muted."

def unmute():
    vol = get_audio_volume()
    if vol:
        vol.SetMute(0, None)
    else:
        # Fallback to volume adjust trick
        _press_key(VK_VOLUME_UP)
        _press_key(VK_VOLUME_DOWN)
    return "System audio restored."
