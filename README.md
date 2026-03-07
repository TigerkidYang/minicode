# Minicode

Minicode is an elite AI coding agent designed to assist with software engineering tasks autonomously through a command-line interface.

## Features

- **Autonomous Task Execution**: Capable of reading, writing, and editing code independently.
- **Tool Integration**: Equipped with specialized tools for file operations, code searching, and system command execution.
- **Self-Awareness**: Capable of analyzing and modifying its own codebase.
- **Professional Objectivity**: Focuses on technical accuracy and direct problem-solving.

## Project Structure

- `main.py`: The entry point of the application, handling the CLI loop.
- `agent.py`: Contains the `MinicodeAgent` class, which manages the conversation flow and tool dispatching.
- `provider.py`: Interfaces with the LLM (currently configured for OpenRouter).
- `prompts.py`: Defines the system instructions and behavioral guidelines.
- `tools/`: A collection of atomic tools:
  - `read.py`: Tool for reading file contents.
  - `write.py`: Tool for creating new files.
  - `edit.py`: Tool for precise search-and-replace edits in existing files.
  - `search.py`: Tool for searching code across the directory.
  - `bash.py`: Tool for executing system commands.

## Getting Started

### Prerequisites

- Python 3.12+
- An API key for OpenRouter (or a compatible OpenAI-like provider).

### Installation

1. Clone the repository.
2. Create a `.env` file in the root directory and add your API key:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```
3. Install dependencies (if any).

### Usage

Run the agent using:
```bash
python main.py
```

## License

This project is licensed under the terms specified in the `LICENSE` file.

---

[中文版说明 (Chinese Version)](./README_CN.md)
