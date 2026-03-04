import os

def read_file(filepath: str) -> str:

    if not os.path.exists(filepath):
        return "Error: File don't exist."
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    except Exception as e:
        return f"Error: Fail to read file - {str(e)}"
    
READ_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read full content of local file. Use this tool whenever you need to check out code, config or any text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "The path or relative path of the file to read. Such as './main.py' or '/Users/xxx/project/app.py'.",
                }
            },
            "required": ["filepath"],
        }
    }
}