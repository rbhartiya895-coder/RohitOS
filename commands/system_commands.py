import os
import ctypes

try:
    from pycaw.pycaw import AudioUtilities
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False
    print("Warning: pycaw not installed. Volume mute will use fallback.")

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False
    print("Warning: screen-brightness-control not installed. Brightness controls will use fallback.")

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

def get_volume():
    if not PYCAW_AVAILABLE:
        return "Cannot read volume without pycaw module."
    vol = get_audio_volume()
    if vol:
        scalar = vol.GetMasterVolumeLevelScalar()
        level = int(round(scalar * 100))
        return f"Current volume is {level} percent."
    return "Failed to get current volume."

def set_volume(level):
    if not PYCAW_AVAILABLE:
        return "Cannot set exact volume without pycaw module."
    level = max(0, min(100, int(level)))
    vol = get_audio_volume()
    if vol:
        vol.SetMasterVolumeLevelScalar(level / 100.0, None)
        return f"Volume set to {level} percent."
    return "Failed to set volume."

def change_volume_relative(amount):
    if not PYCAW_AVAILABLE:
        return "Cannot change volume relative without pycaw module."
    vol = get_audio_volume()
    if vol:
        scalar = vol.GetMasterVolumeLevelScalar()
        current = int(round(scalar * 100))
        new_level = current + int(amount)
        new_level = max(0, min(100, new_level))
        vol.SetMasterVolumeLevelScalar(new_level / 100.0, None)
        return f"Volume set to {new_level} percent."
    return "Failed to change volume."

# --------------------------------
# BRIGHTNESS CONTROL
# --------------------------------

def get_brightness():
    if not SBC_AVAILABLE:
        return "Brightness control is not supported on this display."
    try:
        current = sbc.get_brightness()[0]
        return f"Current brightness is {current} percent."
    except Exception:
        return "Brightness control is not supported on this display."

def set_brightness(level):
    if not SBC_AVAILABLE:
        return "Brightness control is not supported on this display."
    try:
        level = max(0, min(100, int(level)))
        sbc.set_brightness(level)
        return f"Brightness set to {level} percent."
    except Exception:
        return "Brightness control is not supported on this display."

def brightness_up():
    if not SBC_AVAILABLE:
        return "Brightness control is not supported on this display."
    try:
        current = sbc.get_brightness()[0]
        new_level = min(100, current + 10)
        sbc.set_brightness(new_level)
        return f"Brightness increased to {new_level} percent."
    except Exception:
        return "Brightness control is not supported on this display."

def brightness_down():
    if not SBC_AVAILABLE:
        return "Brightness control is not supported on this display."
    try:
        current = sbc.get_brightness()[0]
        new_level = max(0, current - 10)
        sbc.set_brightness(new_level)
        return f"Brightness decreased to {new_level} percent."
    except Exception:
        return "Brightness control is not supported on this display."
