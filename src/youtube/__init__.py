"""YouTube content generator"""

from typing import List, Dict

class YouTubeGenerator:
    """YouTube content generator"""

    def __init__(self, api_client):
        self.api = api_client

    def generate_title(self, subtitles: List[str], summary: str) -> str:
        """Generate title suggestions"""
        prompt = f"""You are a YouTube content strategist. Based on the following video subtitle content, generate 5 attractive video titles.

## Video Summary:
{summary}

## Subtitle Clips:
{chr(10).join(subtitles[:20])}

## Requirements:
1. Titles should be eye-catching but not clickbait
2. Include keywords
3. Suitable for tech/technology videos
4. Concise and powerful

## Output Format:
Output titles directly, one per line, numbered 1-5. No other content."""

        response = self.api.chat(prompt)
        return response

    def generate_description(self, subtitles: List[str], title: str) -> str:
        """Generate video description"""
        prompt = f"""You are a YouTube content operations expert. Based on the following information, generate a professional video description.

## Video Title:
{title}

## Subtitle Content:
{chr(10).join(subtitles[:30])}

## Requirements:
1. Description should be professional and attractive
2. Include chapter timestamps
3. Add appropriate emojis
4. SEO-friendly
5. Length 200-500 characters

Output description directly, no other format."""

        response = self.api.chat(prompt)
        return response

    def generate_chapters(self, subtitles: List[str]) -> str:
        """Generate chapters"""
        prompt = f"""You are a video editing expert. Based on the following subtitle content, identify the main chapters of the video.

## Subtitles:
{chr(10).join(subtitles[:50])}

## Requirements:
1. Identify 3-8 main chapters
2. Provide start timestamp for each chapter
3. Chapter titles should be concise

## Output Format:
Output chapters directly, one per line, format: "timestamp - title", e.g. "0:00 Opening intro". No other content."""

        response = self.api.chat(prompt)
        return response

    def generate_keywords(self, subtitles: List[str], title: str) -> str:
        """Generate SEO keywords"""
        prompt = f"""You are an SEO expert. Based on the following content, generate keywords and tags suitable for YouTube.

## Title:
{title}

## Subtitles:
{chr(10).join(subtitles[:30])}

## Requirements:
1. Generate 10-20 keywords
2. Include short-tail and long-tail keywords
3. Consider search volume
4. YouTube algorithm friendly

Output keywords and tags separated by commas. No other content."""

        response = self.api.chat(prompt)
        return response
