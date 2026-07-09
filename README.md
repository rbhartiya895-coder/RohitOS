# RohitOS

**RohitOS** is a modular AI assistant and early-stage AI operating system prototype built in Python. Designed as a personal desktop assistant, RohitOS focuses on providing a stable, voice-controlled interface to interact with your computer, manage workflows, and eventually evolve into a fully autonomous workflow automation engine.

## Current Features

- **Voice System**: Wake-word activation, dual speech recognition (Google Cloud & Local Faster-Whisper), and dual text-to-speech (Sarvam AI cloud & local PyTTSx3).
- **Desktop Automation**: Launch applications (Notepad, VS Code, Chrome, etc.), control system volume, and manage basic system states (Sleep, Lock).
- **Browser & Web Control**: Launch specific websites and perform Google/YouTube searches.
- **File & Folder Management**: Create and delete directories safely within a designated workspace.
- **Study & Document Mode**: Extract text from PDFs and use LLMs to summarize them or extract key points.
- **Persistent Memory**: Basic fact storage system allowing the assistant to remember and recall user information across sessions.

## Folder Structure

```plaintext
RohitOS/
├── commands/       # Modular command implementations (apps, files, web, system)
├── core/           # Core routing, memory management, session state, and AI engine
├── voice/          # Microphone lifecycle, STT, and TTS engines
├── docs/           # Internal documentation and project context
├── data/           # (Generated) Local JSON storage for memory and sessions
└── main.py         # Entry point and continuous listening loop
```

## Installation & Setup

### Prerequisites
- **OS**: Windows (Relies on Windows-specific UI automation and system commands).
- **Python**: Python 3.12 or higher.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/RohitOS.git
cd RohitOS
```

### 2. Install Dependencies
Install the required packages. *(Note: Some dependencies like `faster-whisper` and `pycaw` are required for local voice and system controls).*
```bash
pip install -r requirements.txt
pip install faster-whisper numpy pycaw screen-brightness-control
```

### 3. Environment Variables
Create a `.env` file in the root directory and add the necessary API keys for cloud capabilities:
```env
# Required for AI chat and document summarization (Gemini 2.5 Flash)
GEMINI_API_KEY=your_gemini_api_key_here

# Required for high-quality Cloud TTS
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_SPEAKER=rahul  # Optional (e.g., rahul, priya)
```

## Running RohitOS

You can launch the assistant via the command line:

```bash
# Voice Mode (Requires Microphone)
python main.py

# Text Mode (Type commands manually)
python main.py --text
```

Alternatively, on Windows, you can double-click `start_rohitos.bat`.

## Example Commands

Once active, use one of the wake words (`hey jarvis`, `hey rohit`, `jarvis`, `rohit`) followed by your command:

- **Web & Apps**: `"open youtube"`, `"open notepad"`, `"search google for python tutorials"`
- **Files**: `"create folder movies"`, `"delete folder movies"`
- **System**: `"volume up"`, `"volume down"`, `"lock computer"`
- **Study**: `"summarize this pdf"` (Requires an active PDF file context)
- **Memory**: `"remember my favorite color is blue"`, `"what is my favorite color"`, `"show memory"`
- **Control**: `"go to sleep"`, `"stop listening"`

## Technologies Used

- **Core**: Python 3.12
- **AI & LLM**: Google GenAI (`gemini-2.5-flash`)
- **Speech Recognition**: `speech_recognition`, `faster-whisper`
- **Text-to-Speech**: `pyttsx3` (SAPI5), Sarvam AI
- **Automation**: `uiautomation`, OS native system calls

## Current Limitations

- **Platform Restriction**: Strictly bound to Windows environments due to hardcoded API calls (`rundll32`, `taskkill`).
- **Synchronous Execution**: Currently lacks asynchronous thread management, causing the system to freeze while executing certain tasks (like reading long summaries aloud).
- **Hardware Intensive**: Local Whisper STT inference runs on the CPU (`int8`), which can spike CPU usage on older machines.

## Roadmap

RohitOS is currently in **Phase 1: Foundation Stability**. 
- **Phase 1**: Stabilize routing, memory persistence, and basic voice command loops.
- **Phase 2 (Future)**: Introduce contextual conversations, offline AI support, and async listening.
- **Phase 3 (Future)**: Build the automation system (browser automation, workflow pipelines).
- **Phase 4 (Future)**: Full AI OS capabilities (Local LLMs, autonomous agents, plugin marketplace).

## License

*(License to be determined. All rights reserved by the author.)*
