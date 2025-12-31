
import re

input_file = 'ko.srt'
output_file = 'ko.srt'

def parse_and_renumber(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Split by double newlines to separate blocks
    # Using regex to handle potential variances in spacing
    blocks = re.split(r'\n\s*\n', content.strip())
    
    new_content = []
    current_index = 1
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            # We assume the first line is the index, second is timestamp, rest is text
            # We replace the first line with the new index
            timestamp = lines[1]
            text = '\n'.join(lines[2:])
            
            new_block = f"{current_index}\n{timestamp}\n{text}\n"
            new_content.append(new_block)
            current_index += 1
            
    return new_content

def save_srt(blocks, filename):
    with open(filename, 'w') as f:
        f.write('\n'.join(blocks))

try:
    new_blocks = parse_and_renumber(input_file)
    save_srt(new_blocks, output_file)
    print(f"Successfully renumbered {len(new_blocks)} subtitles.")
except Exception as e:
    print(f"Error: {e}")
