# Twin - Your AI Command Line Companion

Twin is a powerful AI-driven command-line companion that connects to a locally running Ollama API to process natural language commands and convert them into executable command-line instructions.

## Overview

Unlike the previous prototype which used pattern matching, this implementation:

1. Connects to a locally running Ollama LLM (Large Language Model)
2. Sends your natural language requests to the model
3. Parses the AI-generated response into executable commands
4. Allows you to review and execute the suggested commands

## Requirements

- [Ollama](https://ollama.ai/) installed and running locally
- Python 3.6 or higher
- `requests` library (`pip install requests`)

## Setup

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Start Ollama and make sure it's running on http://localhost:11434
3. Pull the Llama3 model (or another model of your choice):
   ```
   ollama pull llama3
   ```

## Usage

### Windows

Double-click the `run_twin.bat` file or run:

```
python twin.py
```

### Linux/macOS

Run the shell script:

```bash
chmod +x run_twin.sh
./run_twin.sh
```

Or run directly:

```bash
python3 twin.py
```

## Example Commands

You can ask the AI assistant to help with various system tasks using natural language. For example:

- "Install Node.js and npm"
- "Create a new Python virtual environment in the current directory"
- "Show me system information"
- "Find all PDF files in my Documents folder"
- "Set up a basic web server in the current directory"
- "Create a backup of my project folder"

## How It Works

1. Your natural language request is sent to the Ollama API
2. The AI model generates appropriate command-line commands
3. The assistant displays the commands and asks for your confirmation
4. You can choose to run all commands, run a specific command, or skip execution
5. The assistant executes the selected commands and shows the output

## Customization

### Changing the Model

You can modify the script to use a different Ollama model by changing the `model` parameter in the `OllamaLinuxAssistant` initialization.

### System Prompt

The system prompt in the script instructs the AI how to respond. You can modify it to change the behavior of the assistant.

## Security Considerations

- Always review commands before executing them
- The assistant will warn you about potentially dangerous operations
- All processing happens locally on your machine for privacy

## Limitations

- The quality of commands depends on the capabilities of the Ollama model
- Complex tasks might require multiple interactions
- The assistant doesn't maintain state between commands (no memory of previous commands)

## Future Improvements

- Add command history and context awareness
- Implement environment variable management
- Create a proper Linux distribution with this assistant integrated
- Add a graphical user interface
