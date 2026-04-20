#!/usr/bin/env python3
"""
Subtitle Project - AI Subtitle Proofreading & YouTube Content Generation
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.subtitle import load_subtitle, save_subtitle, SubtitleCorrector
from src.subtitle.minimax import get_api_client
from src.youtube import YouTubeGenerator
from src.config import load_config, save_config, get_config_path

def setup_mode():
    """Setup mode - initial configuration"""
    print("=" * 50)
    print("Subtitle Project - Setup Mode")
    print("=" * 50)

    config = load_config()

    if config.get('api_key'):
        print(f"\nCurrent API Key: {config['api_key'][:10]}...")
        change = input("Change? (y/n): ").strip().lower()
        if change != 'y':
            print("Skip")
        else:
            api_key = input("Enter API Key: ").strip()
            config['api_key'] = api_key
    else:
        api_key = input("Enter API Key: ").strip()
        config['api_key'] = api_key

    print(f"\nCurrent API URL: {config.get('api_url', 'https://api.minimax.chat/v1')}")
    change = input("Change? (y/n): ").strip().lower()
    if change == 'y':
        api_url = input("Enter API URL (Enter for default): ").strip()
        config['api_url'] = api_url or "https://api.minimax.chat/v1"

    print(f"\nCurrent Model: {config.get('model', 'abab6.5s-chat')}")
    change = input("Change? (y/n): ").strip().lower()
    if change == 'y':
        model = input("Enter Model (Enter for default): ").strip()
        config['model'] = model or "abab6.5s-chat"

    save_config(config)
    print("\n[OK] Config saved!")
    print(f"   Config file: {get_config_path()}")

def auto_mode(input_dir="input", output_dir="output"):
    """Auto mode"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    srt_files = list(input_path.glob("*.srt")) + list(input_path.glob("*.vtt"))

    if not srt_files:
        print(f"[X] No subtitle files found in {input_path}")
        return

    print("\n" + "=" * 50)
    print("Found subtitle files:")
    print("=" * 50)
    for i, f in enumerate(srt_files, 1):
        print(f"  {i}. {f.name}")
    print(f"  0. Exit")
    print("=" * 50)

    choice = input("\nSelect file (number): ").strip()

    if choice == '0':
        print("Exit")
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(srt_files):
            print("Invalid selection")
            return

        selected_file = srt_files[idx]
    except ValueError:
        print("Invalid input")
        return

    process_file(selected_file, output_path)

def process_file(subtitle_file, output_path):
    """Process single file"""
    print(f"\n[>>] Processing: {subtitle_file.name}")

    config = load_config()
    if not config.get('api_key'):
        print("[X] Run setup mode first to set API Key")
        print("   venv\\Scripts\\python main.py --setup")
        return

    api_client = get_api_client(
        config['api_key'],
        config.get('api_url', 'https://api.minimax.chat/v1'),
        config.get('model', 'abab6.5s-chat')
    )

    corrector = SubtitleCorrector(api_client)
    corrector.load_frequently_used_terms('dict/frequently_used_terms.json')
    corrector.load_corrections('dict/corrections.json')
    youtube_gen = YouTubeGenerator(api_client)

    print("   [..] Loading subtitles...")
    subtitles = load_subtitle(str(subtitle_file))
    print(f"   Loaded {len(subtitles)} subtitle entries")

    video_name = subtitle_file.stem
    video_output = output_path / video_name
    video_output.mkdir(parents=True, exist_ok=True)

    # 1. Proofread
    print("\n   [..] Proofreading subtitles...")
    result = corrector.correct(subtitles)

    if 'corrected_texts' in result:
        corrected_subs = []
        for i, text in enumerate(result['corrected_texts']):
            if i < len(subtitles):
                corrected_subs.append(subtitles[i])
                corrected_subs[-1].text = text

        output_file = video_output / f"{video_name}_corrected.srt"
        save_subtitle(corrected_subs, str(output_file))
        print(f"   [OK] Subtitles saved: {output_file.name}")

    report_file = video_output / "correction_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"   [OK] Report: {report_file.name}")

    # 2. YouTube content
    print("\n   [..] Generating YouTube content...")
    text_lines = [sub.text for sub in subtitles]

    print("   [..] Generating title...")
    titles_text = youtube_gen.generate_title(text_lines, "Tech Video")
    main_title = titles_text.split('\n')[0] if titles_text.strip() else "Video"
    if main_title and main_title[0].isdigit():
        main_title = main_title.split('.', 1)[-1].strip() if '.' in main_title else main_title

    print("   [..] Generating description...")
    desc_text = youtube_gen.generate_description(text_lines, main_title)

    print("   [..] Generating chapters...")
    chapters_text = youtube_gen.generate_chapters(text_lines)

    print("   [..] Generating keywords...")
    keywords_text = youtube_gen.generate_keywords(text_lines, main_title)

    youtube_file = video_output / "youtube_info.txt"
    with open(youtube_file, 'w', encoding='utf-8') as f:
        f.write("=== Video Title ===\n")
        f.write(titles_text + "\n\n")
        f.write("=== Video Description ===\n")
        f.write(desc_text + "\n\n")
        f.write("=== Chapters ===\n")
        f.write(chapters_text + "\n\n")
        f.write("=== Keywords/Tags ===\n")
        f.write(keywords_text + "\n")
    print(f"   [OK] YouTube info: {youtube_file.name}")

    print(f"\n[OK] Done! Output: {video_output}")

def main():
    parser = argparse.ArgumentParser(description='Subtitle Project')
    parser.add_argument('--setup', '-s', action='store_true', help='Setup mode - configure API')
    parser.add_argument('--input', '-i', help='Input file')
    parser.add_argument('--output', '-o', default='output', help='Output directory')
    parser.add_argument('--auto', '-a', action='store_true', help='Auto mode - from input folder')

    args = parser.parse_args()

    if args.setup:
        setup_mode()
    elif args.auto or (not args.input):
        auto_mode("input", args.output)
    else:
        process_file(Path(args.input), Path(args.output))

if __name__ == '__main__':
    main()
