import os

def edit_file(filepath: str, old_code: str, new_code: str) -> str:

    if not os.path.exists(filepath):
        return f"Error: File {filepath} does not exist."
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_code not in content:
            return "Error: `old_code` exact match not found in file. Please read the file again and provide the EXACT code block you want to replace, including all whitespace and indentation."
        
        updated_content = content.replace(old_code, new_code, 1)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return f"Success: File '{filepath}' has been partially updated."
    
    except Exception as e:
        return f"Error: Failed to edit file '{filepath}' - {str(e)}"
    
EDIT_FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "edit_file",
        "description": "Partially update an existing file using Search and Replace. Use this instead of write_file for small changes in large files. You MUST provide the EXACT existing code block to be replaced.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file to edit."
                },
                "old_code": {
                    "type": "string",
                    "description": "The EXACT existing code block in the file that you want to replace. Must include exact indentation and line breaks."
                },
                "new_code": {
                    "type": "string",
                    "description": "The new code block that will replace the old_code."
                }
            },
            "required": ["filepath", "old_code", "new_code"]
        }
    }
}