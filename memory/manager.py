import json
import os
from memory.compaction import compact_if_needed

class MemoryManager:
    def __init__(self, system_prompt: str, max_messages: int = 15):
        self.system_prompt = {"role": "system", "content": system_prompt}
        self.summary = ""
        self.working_memory = []
        self.max_messages = max_messages

    def add_message(self, message):
        self.working_memory.append(message)

    def get_context(self) -> list:
        context = [self.system_prompt]
        if self.summary:
            context.append({
                "role": "system",
                "content": f"[SYSTEM NOTE - PREVIOUS CONTEXT SUMMARY]\n{self.summary}"
            })
        context.extend(self.working_memory)
        return context

    def step(self, provider):
        self.working_memory, self.summary = compact_if_needed(
            provider, 
            self.working_memory, 
            self.summary, 
            self.max_messages
        )

    def save_session(self, session_id: str = "default"):
        os.makedirs(".sessions", exist_ok=True)
        filepath = f".sessions/{session_id}.json"
        try:
            dump_data = {
                "summary": self.summary,
                "working_memory": [
                    msg if isinstance(msg, dict) else msg.model_dump() 
                    for msg in self.working_memory
                ]
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dump_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_session(self, session_id: str = "default"):
        filepath = f".sessions/{session_id}.json"
        if not os.path.exists(filepath):
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.summary = data.get("summary", "")
                self.working_memory = data.get("working_memory", [])
            print(f"[Memory] Session '{session_id}' loaded.")
        except Exception:
            pass