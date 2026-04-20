"""Configuration management"""
import os
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent.parent / "config.json"

def get_config_path():
    return str(CONFIG_FILE)

def load_config():
    """Load configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Create from template if not exists
    template_file = CONFIG_FILE.parent / "config.json.template"
    if template_file.exists():
        with open(template_file, 'r', encoding='utf-8') as f:
            template = json.load(f)
    else:
        template = {
            'api_key': '',
            'api_url': '',
            'model': ''
        }

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    return template

def save_config(config):
    """Save configuration"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# Legacy interface
API_KEY = load_config().get('api_key', '')
API_BASE = load_config().get('api_url', 'https://api.minimax.io/anthropic')
MODEL = load_config().get('model', 'MiniMax-M2.5')
