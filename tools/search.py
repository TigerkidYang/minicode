import os

def search_code(directory: str, keyword: str) -> str:

    if not os.path.exists(directory):
        return f"Error: Directory {directory} does not exist."
    
    IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', 'env', 'build', 'dist'}

    results = []
    match_count = 0
    MAX_MATCHES = 50

    try:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.html', '.css', '.md', '.txt', '.json', '.c', '.cpp', '.h', '.rs', '.go')):
                    filepath = os.path.join(root, file)

                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if keyword in line:
                                    rel_path = os.path.relpath(filepath, directory)
                                    results.append(f"{rel_path}:{line_num}:{line.strip()}")
                                    match_count += 1

                                    if match_count >= MAX_MATCHES:
                                        results.append(f"\n... Reached maximum of {MAX_MATCHES} matches. Please be more specific.")
                                        return "\n".join(results)
                    except Exception:
                        continue
        if not results:
            return f"No matches found for keyword: '{keyword}' in directory: '{directory}'"
            
        return "\n".join(results)
    
    except Exception as e:
        return f"Error while searching: {str(e)}."
    

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_code",
        "description": "Search for a specific string or keyword across all text/code files in a directory. Returns the file path, line number, and the exact line of code. Use this to quickly find where a function, variable, or text is defined or used.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory path to search in (e.g., '.' for current directory)."
                },
                "keyword": {
                    "type": "string",
                    "description": "The specific string or keyword to search for."
                }
            },
            "required": ["directory", "keyword"]
        }
    }
}