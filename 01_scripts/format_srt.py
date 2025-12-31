
import re
import os

def main():
    target_dir = "/Users/taku/Programming/字幕翻訳"
    # Find the file ensuring we handle unicode normalization correctly by picking the existing file
    files = os.listdir(target_dir)
    target_filename = None
    for f in files:
        # Match roughly the name based on known parts if exact match fails, but try to find the one we saw
        if f.endswith(".srt") and ("류타쿠" in f or "류타쿠" in f):
            target_filename = f
            break
            
    if not target_filename:
        print("Error: Could not find the input file.")
        return

    input_path = os.path.join(target_dir, target_filename)
    # Output file: Let's use a name that implies fixed format
    output_path = os.path.join(target_dir, "ryutaku_file_1_fixed.srt")
    
    print(f"Processing: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    entries = []
    current_entry = None
    
    # Timestamp pattern: 00:00:11:26 - 00:00:14:21
    # Allows for possible variations in spacing
    ts_pattern = re.compile(r'^\s*\d{2}:\d{2}:\d{2}:\d{2}\s*-\s*\d{2}:\d{2}:\d{2}:\d{2}\s*$')
    
    for line in lines:
        stripped = line.strip()
        # Check if line is a timestamp
        if ts_pattern.match(stripped):
            if current_entry:
                entries.append(current_entry)
            current_entry = {'timestamp': stripped, 'text': []}
        else:
            if current_entry is not None:
                # If it's not a timestamp, and we are inside an entry, it's potentially text.
                # Only add if not empty. The source file uses empty lines as delimiters.
                if stripped:
                    current_entry['text'].append(line.rstrip())
    
    # Append the last entry
    if current_entry:
        entries.append(current_entry)
        
    print(f"Found {len(entries)} subtitle blocks.")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, entry in enumerate(entries, 1):
            f.write(f"{idx}\n")
            f.write(f"{entry['timestamp']}\n")
            for text_line in entry['text']:
                f.write(f"{text_line}\n")
            f.write("\n")
            
    print(f"Successfully created: {output_path}")

if __name__ == "__main__":
    main()
