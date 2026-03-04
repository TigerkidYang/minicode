import os

def write_file(filepath: str, content: str) -> str:
    try:
        directory = os.path.dirname(filepath)
        
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"Success: File '{filepath}' has been written."
        
    except Exception as e:
        return f"Error: Failed to write file '{filepath}' - {str(e)}"

WRITE_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Create a new file or completely overwrite an existing file. This is the primary way for you to write or modify code. Please provide the complete file content, as this will overwrite the file entirely.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The absolute or relative path of the file to write. Such as './src/utils.py'."
                },
                "content": {
                    "type": "string",
                    "description": "The complete source code or text content to be written into the file."
                }
            },
            "required": ["filepath", "content"]
        }
    }
}