import os
from dotenv import load_dotenv
from agent import MinicodeAgent

load_dotenv()

def main():
    print("Welcome to Minicode!")
    print("Type 'exit' or 'quit' to close.\n")
    print("-" * 50)

    agent = MinicodeAgent()

    while True:
        try:
            user_input = input("\n You: ")
            
            if user_input.strip().lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
            
            if not user_input.strip():
                continue

            agent.run(user_input)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nTerminal Error: {e}")

if __name__ == "__main__":
    main()