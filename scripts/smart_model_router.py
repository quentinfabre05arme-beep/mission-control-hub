"""
Smart Model Router
Automatically switches between models based on task type
"""
import os
import json

class ModelRouter:
    def __init__(self):
        self.config_path = 'C:/Users/quent/.openclaw/workspace/config/model_router.json'
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                self.config = json.load(f)
        else:
            self.config = {
                'models': {
                    'general': 'ollama-cloud/kimi-k2.6',
                    'coding': 'ollama-cloud/qwen3-coder:480b-cloud',
                    'analysis': 'ollama-cloud/kimi-k2.6',
                    'creative': 'ollama-cloud/llama3.3:cloud'
                },
                'auto_switch': True
            }
            self.save_config()
    
    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def detect_task_type(self, message):
        """Detect if a message is coding-related"""
        coding_keywords = [
            'code', 'script', 'function', 'bug', 'error', 'debug',
            'python', 'javascript', 'html', 'css', 'api',
            'import', 'class', 'def ', 'var ', 'const ', 'let ',
            'syntax', 'compile', 'build', 'deploy', 'git',
            'refactor', 'optimize', 'algorithm', 'database',
            'sql', 'json', 'xml', 'http', 'server', 'client'
        ]
        
        message_lower = message.lower()
        
        # Check for coding keywords
        for keyword in coding_keywords:
            if keyword in message_lower:
                return 'coding'
        
        # Check for code blocks
        if '```' in message or '`' in message:
            return 'coding'
        
        return 'general'
    
    def get_model_for_task(self, task_type):
        return self.config['models'].get(task_type, self.config['models']['general'])

if __name__ == '__main__':
    router = ModelRouter()
    print("Smart Model Router initialized")
    print(f"Config: {json.dumps(router.config, indent=2)}")
