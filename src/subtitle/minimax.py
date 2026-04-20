"""Mini Max API client (Anthropic-compatible)"""

import requests
import json
import time

class MiniMaxClient:
    """Mini Max API client"""

    def __init__(self, api_key: str, base_url: str = "https://api.minimax.io/anthropic"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = 180  # 3 minutes timeout
        self.max_retries = 3

    def chat(self, prompt: str, model: str = "MiniMax-M2.5", max_tokens: int = 4096) -> str:
        """Send chat request (Anthropic-compatible format)"""
        url = f"{self.base_url}/v1/messages"

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        print(f"[MiniMax] Calling: {url}")
        print(f"[MiniMax] Model: {model}, Timeout: {self.timeout}s")

        for attempt in range(self.max_retries):
            try:
                print(f"[MiniMax] Attempt {attempt + 1}/{self.max_retries}")
                response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
                print(f"[MiniMax] Status: {response.status_code}")

                if response.status_code != 200:
                    print(f"[MiniMax] Error: {response.text}")
                    return json.dumps({"error": response.json()})

                data = response.json()

                if 'content' in data and len(data['content']) > 0:
                    for block in data['content']:
                        if block.get('type') == 'text':
                            return block.get('text', '')

                return json.dumps(data)

            except requests.exceptions.Timeout:
                print(f"[MiniMax] Timeout, attempt {attempt + 1} failed")
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 10
                    print(f"[MiniMax] Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    error_msg = "Timeout after all retries"
                    print(f"[MiniMax] {error_msg}")
                    return json.dumps({"error": error_msg})
            except requests.exceptions.RequestException as e:
                error_msg = f"Request error: {str(e)}"
                print(f"[MiniMax] {error_msg}")
                return json.dumps({"error": error_msg})
            except json.JSONDecodeError as e:
                error_msg = f"JSON decode error: {str(e)}"
                print(f"[MiniMax] {error_msg}")
                return json.dumps({"error": error_msg})

        return json.dumps({"error": "Max retries exceeded"})

def get_api_client(api_key: str, base_url: str = None, model: str = None):
    """Get API client"""
    base_url = base_url or "https://api.minimax.io/anthropic"
    model = model or "MiniMax-M2.5"
    return MiniMaxClient(api_key, base_url)
