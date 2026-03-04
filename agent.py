import json
from provider import LLMProvider
from tools.read import read_file, READ_FILE_TOOL
from tools.write import write_file, WRITE_FILE_TOOL
from tools.bash import execute_bash, BASH_TOOL

class MinicodeAgent:
    
    def __init__(self):
        self.provider = LLMProvider()

        self.system_prompt = "You are MiniCode, an senior programer. You have access to many tools. You should use them to write file, read file, execute code, see the error and fix them autonomously."

        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        self.tools = [READ_FILE_TOOL, WRITE_FILE_TOOL, BASH_TOOL]

        self.tool_map = {
            "read_file": read_file,
            "write_file": write_file,
            "execute_bash": execute_bash
        }
    
    def run(self, user_prompt: str):
        self.messages.append({"role": "user", "content": user_prompt})

        while True:
            print("Thinking...", end="\r", flush=True)

            message = self.provider.chat(self.messages, self.tools)

            print("           ", end='\r', flush=True)

            if message.tool_calls:
                self.messages.append(message)

                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)

                    print(f"Executing: {func_name}")

                    if func_name in self.tool_map:
                        result = self.tool_map[func_name](**args)
                    else:
                        result = f"Error: {func_name} not found."

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                continue
            else:
                reply = message.content
                print(f"MiniCode:\n{reply}\n")
                self.messages.append({"role":"assistant", "content": reply})
                break

                             