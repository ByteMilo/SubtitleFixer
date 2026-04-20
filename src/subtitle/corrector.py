"""AI subtitle proofreading"""

import json
from typing import List, Dict
from .parser import Subtitle

class SubtitleCorrector:
    """Subtitle proofreader"""

    def __init__(self, api_client):
        self.api = api_client
        self.frequently_used_terms = []
        self.corrections = {}

    def load_frequently_used_terms(self, filepath: str):
        """Load frequently used terms"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.frequently_used_terms = data.get('terms', [])

    def load_corrections(self, filepath: str):
        """Load correction mappings"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.corrections = data.get('corrections', {})

    def apply_corrections(self, text: str) -> str:
        """Apply correction mappings to text"""
        for wrong, correct in self.corrections.items():
            text = text.replace(wrong, correct)
        return text

    def build_prompt(self, subtitles: List[Subtitle]) -> str:
        """Build proofreading prompt"""
        text_lines = [self.apply_corrections(sub.text) for sub in subtitles]

        frequently_used_terms_str = ', '.join(self.frequently_used_terms[:30])

        prompt = f"""You are a professional subtitle proofreader. Please proofread the following subtitles.

## Frequently Used Terms (preserve these exact spellings):
{frequently_used_terms_str}

## Rules:
1. Only fix obvious typos and recognition errors
2. Do not change any correct meaning
3. Do not move any timestamp positions
4. Keep the original English/Chinese spelling of terms
5. If unsure, keep the original

## Subtitle Content:
{chr(10).join(text_lines)}

## Output:
Output the proofread subtitle text, one line per entry, in the original order. Only output the proofread text, nothing else."""
        return prompt

    def correct(self, subtitles: List[Subtitle]) -> Dict:
        """Proofread subtitles"""
        prompt = self.build_prompt(subtitles)

        print("[Corrector] Sending to AI for correction...")
        response = self.api.chat(prompt)

        print(f"[Corrector] Response length: {len(response)} chars")

        corrected_lines = [line.strip() for line in response.strip().split('\n') if line.strip()]

        if len(corrected_lines) != len(subtitles):
            print(f"[Corrector] Warning: Expected {len(subtitles)} lines, got {len(corrected_lines)}")
            if len(corrected_lines) < len(subtitles):
                corrected_lines.extend([sub.text for sub in subtitles[len(corrected_lines):]])
            else:
                corrected_lines = corrected_lines[:len(subtitles)]

        return {
            "corrected_texts": corrected_lines,
            "summary": f"Proofreading complete, {len(subtitles)} subtitle entries"
        }
