import re
import os

def parse_srt_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Split strictly by double newlines to verify block count
    # This regex looks for the pattern of a block start
    # specific to the known strict format of ko.srt
    blocks = re.split(r'\n\n', content)
    parsed = []
    for b in blocks:
        lines = b.split('\n')
        if len(lines) < 3:
            continue
        idx = lines[0]
        timestamp = lines[1]
        # Text is lines[2:]
        parsed.append({'idx': idx, 'timestamp': timestamp})
    return parsed

def generate_srt(language_code, translated_lines, template_path='ko.srt', output_dir='multilingual'):
    template = parse_srt_template(template_path)
    if len(template) != len(translated_lines):
        print(f"Error for {language_code}: Template has {len(template)} blocks but translations have {len(translated_lines)} blocks.")
        return

    output_path = os.path.join(output_dir, f"{language_code}.srt")
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, block in enumerate(template):
            f.write(f"{block['idx']}\n")
            f.write(f"{block['timestamp']}\n")
            f.write(f"{translated_lines[i]}\n")
            if i < len(template) - 1:
                f.write("\n")
    print(f"Generated {output_path}")

