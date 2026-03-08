from memory.summary import summarize_memory

def compact_if_needed(provider, working_memory: list, current_summary: str, max_messages: int = 15, keep_recent: int = 10):

    if len(working_memory) <= max_messages:
        return working_memory, current_summary
        
    print("\n[Memory] Context limit reached. Compacting and summarizing...", flush=True)

    to_summarize = working_memory[:-keep_recent]
    retained_memory = working_memory[-keep_recent:]

    new_summary = summarize_memory(provider, to_summarize, current_summary)
    
    print("[Memory] Compaction complete. Brain cleared.\n", flush=True)
    
    return retained_memory, new_summary