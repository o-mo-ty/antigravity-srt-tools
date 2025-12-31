import re
import os

def parse_srt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Simple regex to capture Index and Timestamp
    # Pattern: Digit(s) \n Timestamp --> Timestamp
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})')
    matches = pattern.findall(content)
    return matches

def verify(file1, file2):
    print(f"Verifying {file1} vs {file2}...")
    sr1 = parse_srt(file1)
    sr2 = parse_srt(file2)
    
    if len(sr1) != len(sr2):
        print(f"Error: Block count mismatch! {file1}: {len(sr1)}, {file2}: {len(sr2)}")
        return False
        
    for i, (idx1, time1) in enumerate(sr1):
        idx2, time2 = sr2[i]
        if idx1 != idx2:
            print(f"Error: Index mismatch at block {i+1}. Expected {idx1}, got {idx2}")
            return False
        if time1 != time2:
            print(f"Error: Timestamp mismatch at index {idx1}. Expected {time1}, got {time2}")
            return False

    print("Success: Indices and Timestamps match perfectly.")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        verify(sys.argv[1], sys.argv[2])
    else:
        # Default behavior or usage
        print("Usage: python verify_srt.py <file1> <file2>")
        # For backward compatibility or testing within this session
        if os.path.exists("ja.srt"):
             verify("ko.srt", "ja.srt")

