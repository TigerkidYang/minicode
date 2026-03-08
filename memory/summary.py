from memory.prompts import SUMMARY_PROMPT

def summarize_memory(provider, to_summarize: list, previous_summary: str) -> str:

    prompt = SUMMARY_PROMPT
    
    if previous_summary:
        prompt += f"Here is the existing previous summary, update it with the new logs:\n{previous_summary}\n\n"
        
    prompt += f"New logs to integrate:\n{str(to_summarize)}"

    response = provider.chat([
        {"role": "system", "content": "You are a highly efficient technical summarizer."},
        {"role": "user", "content": prompt}
    ], tools=[])

    return response.content