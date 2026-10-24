#!/usr/bin/env python3
"""
Mito Interactive Wizard
Interactive setup and configuration wizard
"""

import os
import sys
import json
from pathlib import Path



class Wizard:
    def __init__(self):
        self.config = {}
        self.steps = [
            ("welcome", self.step_welcome),
            ("model", self.step_model),
            ("api", self.step_api),
            ("storage", self.step_storage),
            ("done", self.step_done),
        ]
    
    def run(self):
        for name, step in self.steps:
            step()
            if name == "done":
                break
    
    def step_welcome(self):
        print("\n" + "=" * 50)
        print("  Mito AI Toolkit - Setup Wizard")
        print("=" * 50)
        print("\nThis wizard will help you configure Mito.")
        print("Press Enter to continue or 'q' to quit.")
        
        if input("\n> ").lower() == 'q':
            sys.exit(0)
    
    def step_model(self):
        print("\n--- Model Configuration ---")
        
        print("\nDefault model:")
        print("  1. gpt2")
        print("  2. Custom model")
        
        choice = input("\nSelect [1]: ").strip() or "1"
        
        if choice == "1":
            self.config["model"] = {"name": "gpt2"}
        else:
            name = input("Enter model name: ").strip()
            self.config["model"] = {"name": name}
        
        print(f"✓ Default model: {self.config['model']['name']}")
    
    def step_api(self):
        print("\n--- API Configuration ---")
        
        port = input("Port [8000]: ").strip() or "8000"
        host = input("Host [0.0.0.0]: ").strip() or "0.0.0.0"
        
        self.config["api"] = {
            "port": int(port),
            "host": host
        }
        
        enable_auth = input("Enable API key auth? [y/N]: ").strip().lower() == 'y'
        if enable_auth:
            api_key = input("Enter API key: ").strip()
            self.config["api"]["api_key"] = api_key
        
        print(f"✓ API will run on {host}:{port}")
    
    def step_storage(self):
        print("\n--- Storage Configuration ---")
        
        models_dir = input("Models directory [./models]: ").strip() or "./models"
        data_dir = input("Data directory [./data]: ").strip() or "./data"
        
        Path(models_dir).mkdir(parents=True, exist_ok=True)
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        
        self.config["storage"] = {
            "models_dir": models_dir,
            "data_dir": data_dir
        }
        
        print(f"✓ Storage configured")
    
    def step_done(self):
        print("\n" + "=" * 50)
        print("  Configuration Complete!")
        print("=" * 50)
        
        config_path = "mito.yaml"
        
        with open(config_path, 'w') as f:
            import yaml
            yaml.dump(self.config, f, default_flow_style=False)
        
        print(f"\n✓ Config saved to: {config_path}")
        print("\nRun 'mito server' to start the API.")


class InteractiveMode:
    """Interactive chat mode"""
    
    def __init__(self):
        self.history = []
        self.context = {}
    
    def run(self):
        print("\n--- Mito Interactive Mode ---")
        print("Type 'help' for commands, 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input(">>> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                if user_input.lower() == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue
                
                response = self.process_input(user_input)
                print(f"\n{response}\n")
                
                self.history.append({"user": user_input, "response": response})
                
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit.")
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        print("""
Commands:
  help     - Show this help
  history  - Show conversation history
  clear    - Clear screen
  quit     - Exit interactive mode

Examples:
  summarize this text
  what is machine learning?
  translate Hello to Spanish
  analyze sentiment of this product
        """)
    
    def show_history(self):
        print("\n--- Conversation History ---")
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. You: {entry['user']}")
            print(f"   Bot: {entry['response'][:100]}...")
        print()
    
    def process_input(self, text: str) -> str:
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['summarize', 'summary']):
            return self.summarize(text)
        
        if any(kw in text_lower for kw in ['translate', 'translation']):
            return self.translate(text)
        
        if any(kw in text_lower for kw in ['sentiment', 'feel']):
            return self.sentiment(text)
        
        if any(kw in text_lower for kw in ['what is', 'how does', 'explain']):
            return self.qa(text)
        
        return self.generate(text)
    
    def summarize(self, text: str) -> str:
        from python.ai import Summarizer
        summ = Summarizer()
        return summ.summarize(text, max_length=100)
    
    def translate(self, text: str) -> str:
        from python.ai import Translator
        trans = Translator()
        return trans.translate(text)
    
    def sentiment(self, text: str) -> str:
        from python.ai import quick_sentiment
        result = quick_sentiment(text)
        return f"Sentiment: {result['label']} (score: {result['score']:.2f})"
    
    def qa(self, text: str) -> str:
        from python.ai import QAModel
        qa = QAModel()
        result = qa.answer(text, "Mito is an AI toolkit.")
        return result['answer']
    
    def generate(self, text: str) -> str:
        from python.ai import TextGenerator
        gen = TextGenerator()
        return gen.generate_single(text, max_length=100)


def run_wizard():
    wizard = Wizard()
    wizard.run()


def run_interactive():
    interactive = InteractiveMode()
    interactive.run()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'wizard':
            run_wizard()
        elif sys.argv[1] == 'interactive':
            run_interactive()
    else:
        run_interactive()
