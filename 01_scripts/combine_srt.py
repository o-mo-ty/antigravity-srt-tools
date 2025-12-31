import os
import argparse

def combine_srt_chunks(chunk_dir, output_file):
    # Get all chunk files, sorted
    files = sorted([f for f in os.listdir(chunk_dir) if f.startswith("chunk_") and f.endswith(".srt")])
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, filename in enumerate(files):
            filepath = os.path.join(chunk_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read().strip()
                if not content:
                    continue
                
                # If this is not the first file, add a separator
                if i > 0:
                    outfile.write('\n\n')
                
                outfile.write(content)
    
    # Ensure final newline
    with open(output_file, 'a', encoding='utf-8') as outfile:
        outfile.write('\n')
    
    print(f"Combined {len(files)} chunks into {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine SRT chunks into a single file.')
    parser.add_argument('--chunk_dir', default='99_temp/translated_chunks', help='Directory containing chunk files')
    parser.add_argument('--output_file', default='03_output/ja.srt', help='Output SRT file path')
    
    args = parser.parse_args()
    combine_srt_chunks(args.chunk_dir, args.output_file)
