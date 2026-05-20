import datetime
import os
import re
import shutil
import stat
import subprocess
import sys
import webbrowser
from pathlib import Path
from urllib.parse import quote_plus

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


# ==========================================
# CONFIG
# ==========================================

APP_NAME = "RohitOS"
BASE_DIR = Path.cwd().resolve()
TRASH_DIR = BASE_DIR / "logs" / "deleted_items"
VOICE_LANGUAGE = "en-IN"

WAKE_WORDS = [
    "hey jarvis",
    "jarvis",
    "hey rohit",
    "rohit",
    "hey row hit",
    "row hit",
]

WEBSITES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "chatgpt": "https://chatgpt.com",
    "chat gpt": "https://chatgpt.com",
}

WINDOWS_APPS = {
    "calculator": {
        "open": "calc.exe",
        "display": "Calculator",
        "processes": ("CalculatorApp.exe", "calc.exe"),
    },
    "notepad": {
        "open": "notepad.exe",
        "display": "Notepad",
        "processes": ("notepad.exe",),
    },
}

VS_CODE_PHRASES = (
    "vs code",
    "vscode",
    "visual studio code",
)

VS_CODE_PROCESSES = ("Code.exe",)

OPEN_PHRASES = (
    "open",
    "start",
    "launch",
)

CLOSE_PHRASES = (
    "close",
    "stop",
    "quit",
)

CREATE_FOLDER_PHRASES = (
    "create folder",
    "make folder",
    "create directory",
    "make directory",
)

DELETE_FOLDER_PHRASES = (
    "delete folder",
    "remove folder",
    "delete directory",
    "remove directory",
)

OPEN_FOLDER_PHRASES = (
    "open folder",
    "open directory",
)

POLITE_PREFIXES = (
    "can you please ",
    "could you please ",
    "would you please ",
    "please ",
    "can you ",
    "could you ",
    "would you ",
)

INVALID_FOLDER_CHARS = set('<>:"/\\|?*')
WINDOWS_RESERVED_NAMES = {
    "con",
    "prn",
    "aux",
    "nul",
    "com1",
    "com2",
    "com3",
    "com4",
    "com5",
    "com6",
    "com7",
    "com8",
    "com9",
    "lpt1",
    "lpt2",
    "lpt3",
    "lpt4",
    "lpt5",
    "lpt6",
    "lpt7",
    "lpt8",
    "lpt9",
}


class FolderDeletePermissionError(PermissionError):
    def __init__(self, path, original_error):
        super().__init__(str(original_error))
        self.path = Path(path)
        self.original_error = original_error


# ==========================================
# TEXT TO SPEECH
# ==========================================

def create_tts_engine():
    if pyttsx3 is None:
        print(f"[{APP_NAME}]: pyttsx3 is not installed. Voice output disabled.")
        print("Install it with: py -3.12 -m pip install pyttsx3")
        return None

    try:
        text_engine = pyttsx3.init()
        voices = text_engine.getProperty("voices") or []

        if voices:
            text_engine.setProperty("voice", voices[0].id)

        text_engine.setProperty("rate", 175)
        text_engine.setProperty("volume", 1)
        return text_engine

    except Exception as exc:
        print(f"[{APP_NAME}]: Text-to-speech unavailable: {exc}")
        return None


engine = create_tts_engine()


def speak(text):
    print(f"\n[{APP_NAME}]: {text}")

    if engine is None:
        return

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as exc:
        print(f"[{APP_NAME}]: Could not speak text: {exc}")


# ==========================================
# SPEECH RECOGNIZER
# ==========================================

recognizer = sr.Recognizer() if sr is not None else None

if recognizer is not None:
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8


# ==========================================
# TEXT HELPERS
# ==========================================

def contains_phrase(text, phrase):
    pattern = rf"(?<!\w){re.escape(phrase)}(?!\w)"
    return re.search(pattern, text) is not None


def contains_word(text, word):
    return contains_phrase(text, word)


def find_wake_word(text):
    if not text:
        return None

    for wake_word in sorted(WAKE_WORDS, key=len, reverse=True):
        if contains_phrase(text, wake_word):
            return wake_word

    return None


def command_after_wake_word(text):
    wake_word = find_wake_word(text)

    if wake_word is None:
        return None

    pattern = rf"(?<!\w){re.escape(wake_word)}(?!\w)"
    match = re.search(pattern, text)
    if match is None:
        return None

    command = text[match.end():].strip()
    return command or None


def is_wake_word(text):
    return find_wake_word(text) is not None


def normalize_command(command):
    command = (command or "").strip().lower()
    command = re.sub(r"\s+", " ", command)
    command = command.strip(" .?!")
    command = command.replace("chat g p t", "chatgpt")

    inline_command = command_after_wake_word(command)
    if inline_command:
        command = inline_command

    for prefix in POLITE_PREFIXES:
        if command.startswith(prefix):
            command = command[len(prefix):].strip()
            break

    return command


def extract_argument(command, phrases):
    for phrase in phrases:
        pattern = rf"(?<!\w){re.escape(phrase)}(?!\w)"
        match = re.search(pattern, command)
        if match:
            return command[match.end():].strip()

    return ""


# ==========================================
# FILE AND APP HELPERS
# ==========================================

def clean_folder_name(raw_name):
    folder_name = re.sub(r"\s+", " ", raw_name or "").strip().strip(".")
    folder_name = folder_name.strip("'\"")

    for prefix in ("named ", "called "):
        if folder_name.startswith(prefix):
            folder_name = folder_name[len(prefix):].strip()

    if not folder_name:
        return None

    if any(char in INVALID_FOLDER_CHARS for char in folder_name):
        return None

    if folder_name.lower() in WINDOWS_RESERVED_NAMES:
        return None

    if len(folder_name) > 80:
        return None

    return folder_name


def safe_folder_path(folder_name):
    folder_path = (BASE_DIR / folder_name).resolve()

    if folder_path == BASE_DIR or BASE_DIR not in folder_path.parents:
        raise ValueError("Folder must be inside the current project folder.")

    return folder_path


def folder_contains_running_script(folder_path):
    try:
        Path(__file__).resolve().relative_to(folder_path)
        return True
    except ValueError:
        return False


def retry_readonly_remove(function, path, exc_info):
    exc = exc_info if isinstance(exc_info, BaseException) else exc_info[1]

    if not isinstance(exc, PermissionError):
        raise exc

    try:
        os.chmod(path, stat.S_IREAD | stat.S_IWRITE)
        function(path)
    except Exception as retry_exc:
        if isinstance(retry_exc, PermissionError):
            raise FolderDeletePermissionError(path, retry_exc) from retry_exc
        raise retry_exc


def remove_folder(folder_path):
    if folder_contains_running_script(folder_path):
        raise PermissionError("Cannot delete the folder that contains the running assistant.")

    if sys.version_info >= (3, 12):
        shutil.rmtree(folder_path, onexc=retry_readonly_remove)
    else:
        shutil.rmtree(folder_path, onerror=retry_readonly_remove)


def move_folder_to_trash(folder_path):
    if folder_contains_running_script(folder_path):
        raise PermissionError("Cannot move the folder that contains the running assistant.")

    TRASH_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = TRASH_DIR / f"{folder_path.name}_{timestamp}"
    counter = 1

    while destination.exists():
        counter += 1
        destination = TRASH_DIR / f"{folder_path.name}_{timestamp}_{counter}"

    shutil.move(str(folder_path), str(destination))
    return destination


def open_website(name, url):
    try:
        speak(f"Opening {name}")
        opened = webbrowser.open(url)

        if not opened:
            print(f"[{APP_NAME}]: Browser did not confirm opening {url}.")

    except Exception as exc:
        speak(f"Could not open {name} Boss.")
        print(f"[ERROR]: {exc}")


def open_windows_app(executable, display_name):
    if os.name != "nt":
        speak(f"{display_name} command is configured for Windows only.")
        return

    try:
        subprocess.Popen(
            [executable],
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        speak(f"Opening {display_name}")
    except FileNotFoundError:
        speak(f"Could not find {display_name} Boss.")
    except Exception as exc:
        speak(f"Could not open {display_name} Boss.")
        print(f"[ERROR]: {exc}")


def close_processes(process_names, display_name):
    if os.name != "nt":
        speak(f"{display_name} closing is configured for Windows only.")
        return

    closed_any = False

    for process_name in process_names:
        try:
            result = subprocess.run(
                ["taskkill", "/IM", process_name, "/T"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            output = f"{result.stdout}\n{result.stderr}".lower()

            if result.returncode == 0:
                closed_any = True
            elif "not found" not in output and "not running" not in output:
                print(f"[{APP_NAME}]: Could not close {process_name}: {result.stderr.strip()}")

        except subprocess.TimeoutExpired:
            print(f"[{APP_NAME}]: Timed out while closing {process_name}.")
        except Exception as exc:
            print(f"[ERROR]: {exc}")

    if closed_any:
        speak(f"Closing {display_name}")
    else:
        speak(f"{display_name} is not running Boss.")


def find_vs_code_executable():
    for command in ("code.cmd", "code.exe", "code"):
        executable = shutil.which(command)
        if executable:
            return Path(executable)

    candidates = []
    local_app_data = os.environ.get("LOCALAPPDATA")
    program_files = os.environ.get("ProgramFiles")
    program_files_x86 = os.environ.get("ProgramFiles(x86)")

    if local_app_data:
        candidates.append(Path(local_app_data) / "Programs" / "Microsoft VS Code" / "Code.exe")

    if program_files:
        candidates.append(Path(program_files) / "Microsoft VS Code" / "Code.exe")

    if program_files_x86:
        candidates.append(Path(program_files_x86) / "Microsoft VS Code" / "Code.exe")

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def open_vs_code():
    if os.name != "nt":
        speak("VS Code opening is configured for Windows only.")
        return

    executable = find_vs_code_executable()

    if executable is None:
        speak("I could not find VS Code Boss.")
        print(f"[{APP_NAME}]: Install VS Code or add the code command to PATH.")
        return

    try:
        subprocess.Popen(
            [str(executable), "--reuse-window", str(BASE_DIR)],
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        speak("Opening VS Code")
    except Exception as exc:
        speak("Could not open VS Code Boss.")
        print(f"[ERROR]: {exc}")


def close_vs_code():
    close_processes(VS_CODE_PROCESSES, "VS Code")


def open_local_folder(folder_name):
    try:
        folder_path = safe_folder_path(folder_name)

        if not folder_path.exists():
            speak("Folder not found Boss.")
            return

        if not folder_path.is_dir():
            speak("That is not a folder Boss.")
            return

        if os.name == "nt":
            os.startfile(folder_path)
        else:
            subprocess.Popen(["xdg-open", str(folder_path)])

        speak(f"Opening folder {folder_name}")

    except ValueError as exc:
        speak(str(exc))
    except Exception as exc:
        speak("Could not open the folder Boss.")
        print(f"[ERROR]: {exc}")


def search_google(query):
    if not query:
        speak("Please tell me what to search.")
        return

    open_website("Google search", f"https://www.google.com/search?q={quote_plus(query)}")


def search_youtube(query):
    if not query:
        speak("Please tell me what to search on YouTube.")
        return

    open_website(
        "YouTube search",
        f"https://www.youtube.com/results?search_query={quote_plus(query)}",
    )


# ==========================================
# SPEECH INPUT
# ==========================================

def microphone_is_ready():
    if sr is None:
        print(f"[{APP_NAME}]: speech_recognition is not installed.")
        print("Install it with: py -3.12 -m pip install SpeechRecognition")
        return False

    try:
        microphones = sr.Microphone.list_microphone_names()
    except Exception as exc:
        print(f"[{APP_NAME}]: Microphone support is unavailable: {exc}")
        print("Install PyAudio with: py -3.12 -m pip install PyAudio")
        return False

    if not microphones:
        print(f"[{APP_NAME}]: No microphone detected.")
        return False

    return True


def listen(timeout=5, phrase_limit=5, silent=False):
    if sr is None or recognizer is None:
        return None

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit,
            )

        text = recognizer.recognize_google(audio, language=VOICE_LANGUAGE).lower()

        if not silent:
            print(f"\n[You]: {text}")

        return text

    except sr.WaitTimeoutError:
        return None

    except sr.UnknownValueError:
        if not silent:
            print(f"[{APP_NAME}]: Could not understand.")
        return None

    except sr.RequestError as exc:
        if not silent:
            print(f"[{APP_NAME}]: Speech recognition service unavailable: {exc}")
        return None

    except OSError as exc:
        if not silent:
            print(f"[{APP_NAME}]: Microphone error: {exc}")
        return None

    except Exception as exc:
        if not silent:
            print(f"[ERROR]: {exc}")
        return None


# ==========================================
# COMMAND EXECUTION
# ==========================================

def print_help():
    print(
        "\nCommands:\n"
        "  hello / hi\n"
        "  time / date\n"
        "  open google / open youtube / open chatgpt\n"
        "  search google for python tutorials\n"
        "  search youtube for python projects\n"
        "  open calculator / open notepad / open vs code\n"
        "  close calculator / close notepad / close vs code\n"
        "  create folder test\n"
        "  open folder test\n"
        "  delete folder test\n"
        "  confirm delete folder test\n"
        "  go to sleep\n"
        "  exit\n"
    )
    speak("I printed the command list Boss.")


def create_folder_from_command(command):
    raw_name = extract_argument(command, CREATE_FOLDER_PHRASES)
    folder_name = clean_folder_name(raw_name)

    if not folder_name:
        speak("Please tell a valid folder name.")
        return

    try:
        folder_path = safe_folder_path(folder_name)
        already_exists = folder_path.exists()
        folder_path.mkdir(parents=True, exist_ok=True)

        if already_exists:
            speak(f"Folder {folder_name} already exists Boss.")
        else:
            speak(f"Folder {folder_name} created Boss.")

        print(f"[{APP_NAME}]: Folder path: {folder_path}")

    except ValueError as exc:
        speak(str(exc))
    except PermissionError:
        speak("I do not have permission to create that folder Boss.")
    except Exception as exc:
        speak("Could not create the folder Boss.")
        print(f"[ERROR]: {exc}")


def delete_folder_from_command(command):
    raw_name = extract_argument(command, DELETE_FOLDER_PHRASES)
    folder_name = clean_folder_name(raw_name)

    if not folder_name:
        speak("Please tell a valid folder name.")
        return

    confirmed = (
        command.startswith("confirm delete")
        or command.startswith("yes delete")
        or command.startswith("confirm remove")
        or command.startswith("yes remove")
    )

    if not confirmed:
        speak(f"To delete {folder_name}, say confirm delete folder {folder_name}.")
        return

    try:
        folder_path = safe_folder_path(folder_name)

        if not folder_path.exists():
            speak("Folder not found Boss.")
        elif not folder_path.is_dir():
            speak("That is not a folder Boss.")
        else:
            deleted_path = move_folder_to_trash(folder_path)
            speak(f"Folder {folder_name} moved to RohitOS trash Boss.")
            print(f"[{APP_NAME}]: Original folder: {folder_path}")
            print(f"[{APP_NAME}]: Trash folder: {deleted_path}")

    except FolderDeletePermissionError as exc:
        speak("Windows blocked one file inside that folder. Close open files and pause OneDrive sync, then try again Boss.")
        print(f"[{APP_NAME}]: Blocked path: {exc.path}")
        print(f"[ERROR]: {exc.original_error}")
    except PermissionError as exc:
        speak("I still cannot delete that folder. Close it in apps or File Explorer, then try again Boss.")
        print(f"[{APP_NAME}]: Blocked folder: {folder_path}")
        print(f"[ERROR]: {exc}")
        print(f"[{APP_NAME}]: Tip: do not try to delete the folder that contains assistant.py.")
    except ValueError as exc:
        speak(str(exc))
    except Exception as exc:
        speak("Could not delete the folder Boss.")
        print(f"[ERROR]: {exc}")


def execute_command(command):
    command = normalize_command(command)

    if not command:
        speak("Please say a command Boss.")
        return "continue"

    if command in {"help", "commands", "what can you do"}:
        print_help()

    elif contains_word(command, "hello") or contains_word(command, "hi"):
        speak("Hello Boss!")

    elif any(contains_phrase(command, phrase) for phrase in CREATE_FOLDER_PHRASES):
        create_folder_from_command(command)

    elif any(contains_phrase(command, phrase) for phrase in DELETE_FOLDER_PHRASES):
        delete_folder_from_command(command)

    elif any(contains_phrase(command, phrase) for phrase in OPEN_FOLDER_PHRASES):
        raw_name = extract_argument(command, OPEN_FOLDER_PHRASES)
        folder_name = clean_folder_name(raw_name)

        if folder_name:
            open_local_folder(folder_name)
        else:
            speak("Please tell a valid folder name.")

    elif contains_word(command, "time"):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif contains_word(command, "date"):
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {current_date}")

    elif command.startswith("search google for "):
        search_google(command.replace("search google for ", "", 1).strip())

    elif command.startswith("google search for "):
        search_google(command.replace("google search for ", "", 1).strip())

    elif command.startswith("search youtube for "):
        search_youtube(command.replace("search youtube for ", "", 1).strip())

    elif command.startswith("youtube search for "):
        search_youtube(command.replace("youtube search for ", "", 1).strip())

    elif (
        any(contains_word(command, close_phrase) for close_phrase in CLOSE_PHRASES)
        and any(contains_phrase(command, name) for name in WEBSITES)
    ):
        speak("I can close apps, but browser tab closing is not built yet Boss.")

    elif any(contains_phrase(command, name) for name in WEBSITES):
        for name, url in WEBSITES.items():
            if contains_phrase(command, name):
                open_website(name.title(), url)
                break

    elif (
        any(contains_word(command, close_phrase) for close_phrase in CLOSE_PHRASES)
        and any(contains_phrase(command, phrase) for phrase in VS_CODE_PHRASES)
    ):
        close_vs_code()

    elif (
        any(contains_word(command, open_phrase) for open_phrase in OPEN_PHRASES)
        and any(contains_phrase(command, phrase) for phrase in VS_CODE_PHRASES)
    ):
        open_vs_code()

    elif any(contains_phrase(command, name) for name in WINDOWS_APPS):
        for name, app_config in WINDOWS_APPS.items():
            if contains_phrase(command, name):
                if any(contains_word(command, close_phrase) for close_phrase in CLOSE_PHRASES):
                    close_processes(app_config["processes"], app_config["display"])
                else:
                    open_windows_app(app_config["open"], app_config["display"])
                break

    elif "your name" in command or "who are you" in command:
        speak("I am Rohit OS, your assistant.")

    elif (
        "stop listening" in command
        or "go to sleep" in command
        or contains_word(command, "sleep")
    ):
        speak("Going to sleep Boss.")
        return "sleep"

    elif (
        contains_word(command, "shutdown")
        or contains_word(command, "exit")
        or contains_word(command, "quit")
        or "close yourself" in command
    ):
        speak("Shutting down Boss.")
        return "exit"

    else:
        speak(f"I did not understand {command}. Say help to see commands.")

    return "continue"


# ==========================================
# PROGRAM LOOPS
# ==========================================

def run_voice_mode():
    speak("Rohit OS initialized and running.")
    print(f"[{APP_NAME}]: Base folder is {BASE_DIR}")
    print(f"\n[{APP_NAME}]: Waiting for wake word...")

    running = True

    while running:
        heard = listen(timeout=3, phrase_limit=5, silent=True)

        if not is_wake_word(heard):
            continue

        speak("Yes Boss?")
        active = True
        pending_command = command_after_wake_word(heard)

        while active:
            if pending_command:
                command = pending_command
                pending_command = None
                print(f"\n[You]: {command}")
            else:
                print(f"\n[{APP_NAME}]: Listening for command...")
                command = listen(timeout=6, phrase_limit=8, silent=False)

            if command is None:
                continue

            result = execute_command(command)

            if result == "sleep":
                active = False
                print(f"\n[{APP_NAME}]: Waiting for wake word...")
            elif result == "exit":
                running = False
                active = False


def run_text_mode():
    speak("Text mode started. Type help to see commands.")
    print(f"[{APP_NAME}]: Base folder is {BASE_DIR}")

    while True:
        try:
            command = input("\n[You]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n[{APP_NAME}]: Stopped.")
            return

        if not command:
            continue

        result = execute_command(command)

        if result == "exit":
            return

        if result == "sleep":
            speak("Text mode is still ready. Type another command.")


def main():
    force_text_mode = "--text" in sys.argv

    if force_text_mode:
        run_text_mode()
        return

    if microphone_is_ready():
        run_voice_mode()
    else:
        speak("Voice input is unavailable, so I am starting text mode.")
        run_text_mode()


# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n[{APP_NAME}]: Stopped.")
