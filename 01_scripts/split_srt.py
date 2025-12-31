import re
import os

def split_srt(input_file, chunk_size=30, output_dir="chunks"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get blocks (approximately)
    # A more robust regex for SRT blocks
    # Blocks are separated by one or more blank lines.
    # We'll use a regex that looks for the index at the start of a line.
    
    # Standard SRT block format:
    # Index
    # Timestamp
    # Text
    # (Blank line)
    
    # We can split by the pattern: \n\n(?=\d+\n\d{2}:\d{2}:\d{2})
    # But sometimes files are messy.
    
    # simple approach: collect lines until we see a blank line, then that's a block?
    # No, blank lines can be in text (rare but possible). 
    # Reliable split: Look for correct SRT index pattern.
    
    blocks = []
    current_block = []
    
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.isdigit():
            # Potential start of block
            # Check next line for timestamp
            if i + 1 < len(lines) and '-->' in lines[i+1]:
                # It is a start of a block
                if current_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
                
                # Consume block until next double newline or end of file
                # Actually, simpler: just regex split the whole content.
                pass
        current_block.append(lines[i])
        i += 1
    
    if current_block:
         blocks.append("\n".join(current_block))

    # The above loop logic is slightly flawed for robust splitting. 
    # Let's use re.split with a lookahead for Index + Timestamp
    
    # Re-reading content to use regex split
    pattern = re.compile(r'(?=\n\d+\n\d{2}:\d{2}:\d{2})', re.MULTILINE)
    # Note: The first block won't have a preceding newline matching strictly if it's at start of file, 
    # but let's handle that.
    
    raw_blocks = pattern.split(content)
    # Filter out empty strings
    srt_blocks = [b.strip() for b in raw_blocks if b.strip()]

    print(f"Total blocks found: {len(srt_blocks)}")

    for i in range(0, len(srt_blocks), chunk_size):
        chunk = srt_blocks[i:i + chunk_size]
        chunk_num = (i // chunk_size) + 1
        output_filename = os.path.join(output_dir, f"chunk_{chunk_num:03d}.srt")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(chunk))
            f.write("\n") # End with newline
        print(f"Created {output_filename} with {len(chunk)} blocks")

if __name__ == "__main__":
    split_srt("ko.srt", chunk_size=30)
