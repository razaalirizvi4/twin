#!/usr/bin/env python3

"""Twin - Your AI Command Line Companion

This script connects to a locally running Ollama API (http://localhost:11434),
sends user input as prompts, and converts AI responses into executable command-line commands.

Usage:
    python twin.py
    
Requirements:
    - Ollama running locally on port 11434
    - requests library (pip install requests)
"""

import os
import sys
import json
import subprocess
import requests
from typing import Dict, List, Any, Optional

class OllamaLinuxAssistant:
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "gemma3"):
        """
        Initialize the Ollama Linux Assistant
        
        Args:
            ollama_url: URL of the Ollama API
            model: The model to use for generating responses
        """
        self.ollama_url = ollama_url
        self.model = model
        self.api_endpoint = f"{ollama_url}/api/generate"
        self.system_prompt = '''You are Twin, an AI command-line companion. Your task is to convert natural language requests into executable command-line commands.

For each user request:
1. Understand what the user wants to accomplish
2. Generate the appropriate command-line commands to fulfill the request
3. Format your response as a JSON object with the following structure:
   {
     "explanation": "Brief explanation of what the commands will do",
     "commands": ["command1", "command2", ...],
     "warning": "Optional warning about potential risks or side effects"
   }

Only respond with valid JSON. Do not include any other text in your response.
If you are unsure about a command or if it might be dangerous, include a warning.'''
        
        # Check if Ollama is running
        self._check_ollama_connection()
    
    def _check_ollama_connection(self) -> None:
        """
        Check if Ollama API is accessible
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            response.raise_for_status()
            print(f"✓ Connected to Ollama API at {self.ollama_url}")
            print(f"✓ Using model: {self.model}")
        except requests.exceptions.RequestException as e:
            print(f"Error: Could not connect to Ollama API at {self.ollama_url}")
            print(f"Make sure Ollama is running and accessible at {self.ollama_url}")
            print(f"Error details: {e}")
            sys.exit(1)
    
    def send_prompt(self, prompt: str) -> Dict[str, Any]:
        '''Send a prompt to the Ollama API and return the response
        
        Args:
            prompt: The user's natural language request
            
        Returns:
            Parsed JSON response with commands to execute
        '''
        data = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_endpoint, json=data)
            response.raise_for_status()
            response_data = response.json()
            
            # Extract the response text
            response_text = response_data.get("response", "")
            
            # Try to parse the JSON response
            try:
                # Find JSON content (in case there's any extra text)
                json_start = response_text.find('{')
                json_end = response_text.rfind('}')
                
                if json_start >= 0 and json_end >= 0:
                    json_content = response_text[json_start:json_end+1]
                    parsed_response = json.loads(json_content)
                    return parsed_response
                else:
                    # If no JSON found, create a simple response
                    return {
                        "explanation": "Could not parse response as JSON",
                        "commands": [],
                        "warning": f"The model did not return valid JSON. Raw response: {response_text[:100]}..."
                    }
            except json.JSONDecodeError:
                # If JSON parsing fails, create a simple response
                return {
                    "explanation": "Could not parse response as JSON",
                    "commands": [],
                    "warning": f"The model did not return valid JSON. Raw response: {response_text[:100]}..."
                }
                
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama API: {e}")
            return {
                "explanation": "Error communicating with Ollama API",
                "commands": [],
                "warning": str(e)
            }
    
    def execute_command(self, command: str) -> str:
        """
        Execute a shell command and return the output
        
        Args:
            command: The command to execute
            
        Returns:
            Command output as string
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                text=True,
                capture_output=True
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error (code {result.returncode}):\n{result.stderr}"
        except Exception as e:
            return f"Failed to execute command: {e}"

def main():
    """
    Main function to run the AI Linux Assistant
    """
    # ANSI color codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    # Parse command line arguments
    ollama_url = "http://localhost:11434"
    model = "gemma3"
    
    # Initialize the assistant
    assistant = OllamaLinuxAssistant(ollama_url, model)
    
    # Print welcome message
    print(f"{BOLD}{BLUE}Twin{RESET} - Your AI Command Line Companion")
    print(f"Type your requests in natural language or {BOLD}'exit'{RESET} to quit.")
    print(f"Example: 'install nodejs' or 'create a new python virtual environment'")
    print()
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input(f"{BOLD}twin>{RESET} ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            print(f"\n{BLUE}Processing your request...{RESET}")
            
            # Send the prompt to Ollama
            response = assistant.send_prompt(user_input)
            
            # Display the explanation
            if "explanation" in response:
                print(f"\n{BOLD}Understanding:{RESET} {response['explanation']}")
            
            # Display any warnings
            if "warning" in response and response["warning"]:
                print(f"\n{YELLOW}{BOLD}Warning:{RESET} {response['warning']}")
            
            # Display and offer to execute commands
            if "commands" in response and response["commands"]:
                print(f"\n{BOLD}Commands to execute:{RESET}")
                
                for i, cmd in enumerate(response["commands"], 1):
                    print(f"  {i}. {GREEN}{cmd}{RESET}")
                
                # Ask for confirmation
                print("\nOptions:")
                print(f"  {BOLD}run{RESET} - Execute all commands")
                print(f"  {BOLD}run N{RESET} - Execute command number N")
                print(f"  {BOLD}skip{RESET} - Skip execution")
                
                action = input(f"\nWhat would you like to do? [{BOLD}run{RESET}/run N/skip]: ").strip().lower()
                
                if action == "run":
                    # Execute all commands
                    print("\n" + "-" * 50)
                    for cmd in response["commands"]:
                        print(f"\n{BOLD}Executing:{RESET} {cmd}")
                        output = assistant.execute_command(cmd)
                        print(output)
                    print("-" * 50)
                elif action.startswith("run "):
                    # Execute specific command
                    try:
                        cmd_index = int(action.split()[1]) - 1
                        if 0 <= cmd_index < len(response["commands"]):
                            cmd = response["commands"][cmd_index]
                            print("\n" + "-" * 50)
                            print(f"\n{BOLD}Executing:{RESET} {cmd}")
                            output = assistant.execute_command(cmd)
                            print(output)
                            print("-" * 50)
                        else:
                            print(f"\n{RED}Invalid command number.{RESET}")
                    except (ValueError, IndexError):
                        print(f"\n{RED}Invalid input. Please enter a valid command number.{RESET}")
                else:
                    print("\nCommands skipped.")
            else:
                print(f"\n{RED}No commands were generated.{RESET}")
            
            print()  # Add a blank line for readability
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"\n{RED}Error: {e}{RESET}")

if __name__ == "__main__":
    main()