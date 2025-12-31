import re
import os
import argparse

def split_srt(input_file, chunk_size=30, output_dir="chunks"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Re-reading content to use regex split
    pattern = re.compile(r'(?=\n\d+\n\d{2}:\d{2}:\d{2})', re.MULTILINE)
    
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
    parser = argparse.ArgumentParser(description='Split SRT file into chunks.')
    parser.add_argument('input_file', help='Input SRT file path')
    parser.add_argument('--output_dir', default='99_temp/chunks', help='Output directory for chunks')
    parser.add_argument('--chunk_size', type=int, default=30, help='Number of subtitles per chunk')
    
    args = parser.parse_args()
    split_srt(args.input_file, args.chunk_size, args.output_dir)
