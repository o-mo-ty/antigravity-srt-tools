#!/usr/bin/env python3
# compare_srt.py
# 使い方:
#   python3 compare_srt.py 1.srt 2.srt
#   python3 compare_srt.py 1.srt 2.srt --normalize  # 空白等の表記差を無視して比較

#   python3 compare_srt.py ko.srt ja.srt
#   python3 compare_srt.py ko.srt en.srt

import re
import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional

TIMECODE_RE = re.compile(
    r'^\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*'
    r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*(?:,.*)?\s*$'
)

@dataclass
class Cue:
    idx_raw: str          # 行の生テキスト（厳密一致用）
    time_raw: str         # 行の生テキスト（厳密一致用）
    idx: int              # 数値化したインデックス
    start_ms: int         # ミリ秒
    end_ms: int           # ミリ秒

def parse_time_ms(h: str, m: str, s: str, ms: str) -> int:
    return (int(h)*3600 + int(m)*60 + int(s)) * 1000 + int(ms)

def parse_srt(path: str) -> List[Cue]:
    cues: List[Cue] = []
    with open(path, 'r', encoding='utf-8-sig', errors='replace') as f:
        lines = f.read().splitlines()

    i = 0
    n = len(lines)
    while i < n:
        # スキップ空行
        while i < n and lines[i].strip() == "":
            i += 1
        if i >= n:
            break

        idx_line = lines[i]
        i += 1

        # 次はタイムコード行のはず
        if i >= n:
            raise ValueError(f"{path}: インデックス {idx_line!r} の後にタイムコード行がありません")
        time_line = lines[i]
        i += 1

        # タイムコード解析
        m = TIMECODE_RE.match(time_line)
        if not m:
            raise ValueError(f"{path}: タイムコード行の形式が不正: {time_line!r}")

        try:
            idx_val = int(idx_line.strip())
        except ValueError:
            raise ValueError(f"{path}: インデックス行が数値ではありません: {idx_line!r}")

        sh, sm, ss, sms, eh, em, es, ems = m.groups()
        start_ms = parse_time_ms(sh, sm, ss, sms)
        end_ms = parse_time_ms(eh, em, es, ems)

        cues.append(Cue(
            idx_raw=idx_line,
            time_raw=time_line,
            idx=int(idx_val),
            start_ms=start_ms,
            end_ms=end_ms
        ))

        # テキスト行を空行まで飛ばす
        while i < n and lines[i].strip() != "":
            i += 1
        # 空行（ブロック区切り）を1行進める
        if i < n and lines[i].strip() == "":
            i += 1

    return cues

def compare_srt(a_path: str, b_path: str, normalize: bool = False) -> int:
    a = parse_srt(a_path)
    b = parse_srt(b_path)

    exit_code = 0
    problems: List[str] = []

    if len(a) != len(b):
        problems.append(f"キュー数が異なります: {a_path}={len(a)}件, {b_path}={len(b)}件")
        exit_code = 1

    for i in range(min(len(a), len(b))):
        ca, cb = a[i], b[i]

        # インデックス一致
        if normalize:
            idx_equal = (ca.idx == cb.idx)
        else:
            # 文字列として厳密一致（前後空白はSRT的に意味がないのでstripして比較）
            idx_equal = (ca.idx_raw.strip() == cb.idx_raw.strip())

        if not idx_equal:
            problems.append(
                f"[{i+1}番目のキュー] インデックス不一致: {a_path}='{ca.idx_raw}', {b_path}='{cb.idx_raw}'"
            )
            exit_code = 1

        # タイムコード一致
        if normalize:
            time_equal = (ca.start_ms == cb.start_ms and ca.end_ms == cb.end_ms)
        else:
            # 文字列として厳密一致（前後空白のみ無視）
            time_equal = (ca.time_raw.strip() == cb.time_raw.strip())

        if not time_equal:
            problems.append(
                f"[{i+1}番目のキュー] タイムコード不一致:\n"
                f"  {a_path}: {ca.time_raw}\n"
                f"  {b_path}: {cb.time_raw}"
            )
            exit_code = 1

    if exit_code == 0:
        mode = "（厳密一致）" if not normalize else "（正規化一致）"
        print(f"OK: すべてのインデックス番号とタイムコードが一致しました {mode}")
    else:
        print("NG: 不一致があります。")
        for p in problems:
            print("- " + p)

    return exit_code

def main(argv: List[str]) -> int:
    if len(argv) < 3 or len(argv) > 4:
        print("使い方: python compare_srt.py 1.srt 2.srt [--normalize]")
        return 2
    a_path, b_path = argv[1], argv[2]
    normalize = (len(argv) == 4 and argv[3] == "--normalize")
    try:
        return compare_srt(a_path, b_path, normalize=normalize)
    except Exception as e:
        print("エラー:", e)
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))