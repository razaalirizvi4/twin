# Twin - Your AI Command Line Companion

Twin is an AI-powered command-line assistant that converts natural language requests into executable shell commands. It integrates with Ollama to provide a seamless experience for users who want to interact with their command line using natural language.

## Features

- Convert natural language to shell commands
- Execute commands directly or review them first
- Warnings for potentially dangerous operations
- Cross-platform support (Windows, Linux, macOS)

## Prerequisites

- Python 3.6 or higher
- [Ollama](https://ollama.ai/) running locally
- The `gemma3` model installed in Ollama
- Python `requests` library

## Installation

1. Clone this repository or download the files
2. Install the required Python package:
   ```
   pip install requests
   ```
3. Make sure Ollama is running with the `gemma3` model installed

## Usage

### Windows

Run the `run_twin.bat` script or execute:

```
python twin.py
```

### Linux/macOS

Run the `run_twin.sh` script or execute:

```
python twin.py
```

## Example Commands

Once Twin is running, you can type natural language requests like:

- "List all files in the current directory"
- "Create a new directory called projects"
- "Find all text files containing the word 'important'"
- "Show system information"

## License

This project is open source and available under the MIT License.




## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to help improve Twin.