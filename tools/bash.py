import subprocess

def execute_bash(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if result.returncode == 0:
            return output if output else "Success: Command executed with no output."
        else:
            return f"Error (Exit code {result.returncode}):\nStdout: {output}\nStderr: {error}"
            
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out after 120 seconds."
    except Exception as e:
        return f"Error: Failed to execute command - {str(e)}"

BASH_TOOL = {
    "type": "function",
    "function": {
        "name": "execute_bash",
        "description": "Execute a bash or shell command on the local machine. Use this to run scripts, install dependencies, run tests, or inspect directories (e.g., 'ls -la', 'npm install', 'python test.py').",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute."
                }
            },
            "required": ["command"]
        }
    }
}