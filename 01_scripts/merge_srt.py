
import argparse
import re
from datetime import timedelta
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Subtitle:
    index: int
    start: timedelta
    end: timedelta
    text: str

def parse_time(time_str: str) -> timedelta:
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split(',')
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

def format_time(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def read_srt(file_path: str) -> List[Subtitle]:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\n+', content.strip())
    subtitles = []
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            try:
                index = int(lines[0])
                time_line = lines[1]
                start_str, end_str = time_line.split(' --> ')
                start = parse_time(start_str)
                end = parse_time(end_str)
                text = '\n'.join(lines[2:])
                subtitles.append(Subtitle(index, start, end, text))
            except ValueError:
                continue
                
    return subtitles

def merge_subtitles(srt_files: List[str]) -> List[Subtitle]:
    all_subtitles = []
    for file_path in srt_files:
        all_subtitles.extend(read_srt(file_path))

    if not all_subtitles:
        return []

    # Collect all unique time points
    time_points = set()
    for sub in all_subtitles:
        time_points.add(sub.start)
        time_points.add(sub.end)
    
    sorted_points = sorted(list(time_points))
    
    merged_intervals = []
    
    # Create elementary intervals
    for i in range(len(sorted_points) - 1):
        start = sorted_points[i]
        end = sorted_points[i+1]
        
        # Skip zero-duration intervals
        if start == end:
            continue
            
        mid_point = start + (end - start) / 2
        
        active_texts = []
        for sub in all_subtitles:
            if sub.start <= mid_point < sub.end:
                if sub.text not in active_texts: # Avoid duplicates from same file logic if any
                    active_texts.append(sub.text)
        
        if active_texts:
            merged_text = '\n'.join(active_texts)
            merged_intervals.append({'start': start, 'end': end, 'text': merged_text})

    if not merged_intervals:
        return []

    # Combine adjacent intervals with same text
    final_subtitles = []
    current_interval = merged_intervals[0]
    
    for i in range(1, len(merged_intervals)):
        next_interval = merged_intervals[i]
        
        # If text is same and intervals are adjacent (they should be by design of sorted_points), merge
        if current_interval['text'] == next_interval['text']:
            current_interval['end'] = next_interval['end']
        else:
            final_subtitles.append(Subtitle(
                len(final_subtitles) + 1,
                current_interval['start'],
                current_interval['end'],
                current_interval['text']
            ))
            current_interval = next_interval
            
    # Append the last interval
    final_subtitles.append(Subtitle(
        len(final_subtitles) + 1,
        current_interval['start'],
        current_interval['end'],
        current_interval['text']
    ))
    
    return final_subtitles

def write_srt(subtitles: List[Subtitle], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, sub in enumerate(subtitles):
            f.write(f"{i + 1}\n")
            f.write(f"{format_time(sub.start)} --> {format_time(sub.end)}\n")
            f.write(f"{sub.text}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge multiple SRT files.')
    parser.add_argument('--inputs', nargs='+', required=True, help='Input SRT files')
    parser.add_argument('--output', required=True, help='Output SRT file')
    
    args = parser.parse_args()
    
    merged = merge_subtitles(args.inputs)
    write_srt(merged, args.output)
    print(f"Merged {len(args.inputs)} files into {args.output}")
