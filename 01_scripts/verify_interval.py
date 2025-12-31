import re

def parse_srt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newlines to get blocks
    blocks = re.split(r'\n\s*\n', content.strip())
    
    subtitles = {}
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            try:
                index = int(lines[0].strip())
                # Timestamp is lines[1]
                # Text is lines[2:]
                text = '\n'.join(lines[2:])
                subtitles[index] = text
            except ValueError:
                continue
    return subtitles

def main():
    ja_subs = parse_srt('ja.srt')
    ko_subs = parse_srt('ko.srt')
    
    max_index = max(ja_subs.keys())
    
    print(f"{'Index':<6} | {'Japanese':<40} | {'Korean':<40}")
    print("-" * 90)
    
    for i in range(30, max_index + 1, 30):
        ja_text = ja_subs.get(i, "").replace('\n', ' ')
        ko_text = ko_subs.get(i, "").replace('\n', ' ')
        
        # Truncate for display if too long
        if len(ja_text) > 38:
            ja_text = ja_text[:35] + "..."
        if len(ko_text) > 38:
            ko_text = ko_text[:35] + "..."
            
        print(f"{i:<6} | {ja_text:<40} | {ko_text:<40}")

if __name__ == "__main__":
    main()
