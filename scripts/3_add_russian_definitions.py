#!/usr/bin/env python3
"""
ZID: 20260723233029
Description: Populates/updates the Russian column in Goethe German 5000 TSV files 
             using multi-definition Russian fields from the CSV file (Definition 1-3 Russian),
             joining multiple definitions with '; '.
"""

import csv
import os

input_csv = r"U:\voothi\20260716201616-german-5000\20260716200932-goethe-german-5000-ru.de.csv"
target_tsvs = [
    r"U:\voothi\20260716201616-german-5000\20260716200932-goethe-german-5000-ru.de.tsv",
    r"U:\voothi\20260716201616-german-5000\20260716202200-goethe-german-5000-freq-ru.de.tsv"
]

def get_col(row, idx):
    return row[idx].strip() if idx < len(row) else ""

def format_russian_definitions(defs):
    filtered = []
    seen = set()
    for d in defs:
        d_clean = d.strip()
        if d_clean and d_clean not in ("None", "-", "--", "n/a", "null", "не определено", "?"):
            if d_clean not in seen:
                seen.add(d_clean)
                filtered.append(d_clean)
    return "; ".join(filtered)

def main():
    if not os.path.exists(input_csv):
        print(f"Error: Input CSV not found: {input_csv}")
        return

    print(f"Reading CSV from: {input_csv}")
    with open(input_csv, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=";")
        header = next(csv_reader)
        word_idx = header.index("Word")
        pos1_idx = header.index("Part-of-Speech 1")
        def1_ru_idx = header.index("Definition 1 Russian")
        def2_ru_idx = header.index("Definition 2 Russian")
        def3_ru_idx = header.index("Definition 3 Russian")

        csv_rows = list(csv_reader)

    csv_by_word_pos = {}
    csv_by_word = {}

    for r in csv_rows:
        w = get_col(r, word_idx)
        pos1 = get_col(r, pos1_idx)
        defs_ru = [get_col(r, def1_ru_idx), get_col(r, def2_ru_idx), get_col(r, def3_ru_idx)]
        ru_str = format_russian_definitions(defs_ru)

        if w:
            csv_by_word_pos[(w, pos1)] = ru_str
            if w not in csv_by_word or (not csv_by_word[w] and ru_str):
                csv_by_word[w] = ru_str

    for tsv_path in target_tsvs:
        if not os.path.exists(tsv_path):
            print(f"Skipping missing TSV: {tsv_path}")
            continue

        print(f"Processing TSV: {tsv_path}")
        with open(tsv_path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\r\n").split("\t") for line in f]

        if not lines:
            continue

        header_tsv = lines[0]
        if "Russian" not in header_tsv:
            header_tsv.append("Russian")
        ru_col_idx = header_tsv.index("Russian")

        matched_count = 0
        for row in lines[1:]:
            word = get_col(row, 0)
            annot = get_col(row, 1)
            pos = get_col(row, 3)

            ru = csv_by_word_pos.get((annot, pos)) or csv_by_word_pos.get((word, pos))
            if ru is None:
                ru = csv_by_word.get(annot) or csv_by_word.get(word) or ""

            while len(row) <= ru_col_idx:
                row.append("")
            row[ru_col_idx] = ru
            if ru:
                matched_count += 1

        with open(tsv_path, "w", encoding="utf-8", newline="") as f:
            for row in lines:
                f.write("\t".join(row) + "\n")

        print(f"Updated {matched_count}/{len(lines)-1} rows in {os.path.basename(tsv_path)}")

if __name__ == "__main__":
    main()
