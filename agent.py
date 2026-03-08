import json

from provider import LLMProvider

from tools.read import read_file, READ_FILE_TOOL
from tools.write import write_file, WRITE_FILE_TOOL
from tools.bash import execute_bash, BASH_TOOL
from tools.search import search_code, SEARCH_TOOL
from tools.edit import edit_file, EDIT_FILE_TOOL

from prompts import SYSTEM_PROMPT
from memory.manager import MemoryManager

class MinicodeAgent:
    
    def __init__(self):
        self.provider = LLMProvider()
        self.memory = MemoryManager(SYSTEM_PROMPT)
        self.memory.load_session()

        self.tools = [READ_FILE_TOOL, WRITE_FILE_TOOL, BASH_TOOL, SEARCH_TOOL, EDIT_FILE_TOOL]

        self.tool_map = {
            "read_file": read_file,
            "write_file": write_file,
            "execute_bash": execute_bash,
            "search_code": search_code,
            "edit_file": edit_file
        }
    
    def run(self, user_prompt: str):
        self.memory.add_message({"role": "user", "content": user_prompt})
        self.memory.save_session()

        while True:
            self.memory.step(self.provider)
            print("Thinking...", end="\r", flush=True)

            message = self.provider.chat(self.memory.get_context(), self.tools)

            print("           ", end="\r", flush=True)

            if message.tool_calls:
                self.memory.add_message(message)

                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)

                    print(f"Executing: {func_name}")

                    if func_name in self.tool_map:
                        result = self.tool_map[func_name](**args)
                    else:
                        result = f"Error: {func_name} not found."

                    self.memory.add_message({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                    self.memory.save_session()
                continue

            reply = message.content
            print(f"MiniCode:\n{reply}\n")
            self.memory.add_message({"role":"assistant", "content": reply})
            self.memory.save_session()
            break
