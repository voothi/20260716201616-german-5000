#!/usr/bin/env python3
"""
ZID: 20260716213550
Description: Converts the Goethe German 5000 CSV file to a clean 5-column TSV format,
             normalizing noun articles, stripping adjective endings, and merging
             Part-of-Speech columns. The original raw strings are preserved in the
             Annotation column.
"""

import csv
import os
import re

input_path = r"U:\voothi\20260716201616-german-5000\20260716200932-english-deutsch.de.csv"
output_path = r"U:\voothi\20241223170748-kardenwort\data\de\20260716200932-english-deutsch.de.tsv"

def clean_german_lemma(raw_word):
    # Strip parentheticals first to avoid splitting on commas inside them
    cleaned = re.sub(r"\(.*?\)", "", raw_word).strip()
    
    parts = []
    # Split by comma to process each form/variant separately
    for i, part in enumerate(cleaned.split(",")):
        part = part.strip()
        if not part:
            continue
        # Skip suffixes like -e, -en, -̈er, but only if they are not the first item
        if part.startswith("-") and i > 0:
            continue
        # Strip article prefixes from nouns (e.g. "das Jahr" -> "Jahr", "der Mensch" -> "Mensch")
        # but preserve standalone articles (e.g. "der" on its own line)
        match = re.match(r"^(der|die|das)\s+(\S+.*)$", part, re.IGNORECASE)
        if match:
            part = match.group(2).strip()
            
        if part:
            parts.append(part)
    return ", ".join(parts)

def german_sort_key(r):
    w = r["word"].lower()
    w = w.replace("ä", "a").replace("ö", "o").replace("ü", "u").replace("ß", "ss")
    w = re.sub(r"[^a-z0-9\s,]", "", w)
    return (w, r["word"])

def main():
    records = []
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return
        
    print(f"Reading from: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        
        # Identify columns
        word_idx = header.index("Word")
        level_idx = header.index("Level")
        pos_indices = [
            header.index("Part-of-Speech 1"),
            header.index("Part-of-Speech 2"),
            header.index("Part-of-Speech 3")
        ]
        
        for row in reader:
            if not row:
                continue
            
            raw_word = row[word_idx].strip()
            level = row[level_idx].strip()
            
            # Extract lookup keys and keep original string as annotation
            cleaned_word = clean_german_lemma(raw_word)
            annotation = raw_word
            
            # Combine non-empty Part-of-Speech columns
            pos_list = []
            for idx in pos_indices:
                if idx < len(row) and row[idx].strip():
                    pos_list.append(row[idx].strip())
            pos = ", ".join(pos_list)
            
            records.append({
                "word": cleaned_word,
                "annotation": annotation,
                "sense": "",
                "pos": pos,
                "level": level
            })
            
    records.sort(key=german_sort_key)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write to target TSV
    print(f"Writing to: {output_path}")
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write("Word\tAnnotation\tSense\tPart of Speech\tLevel\n")
        for r in records:
            f.write(f"{r['word']}\t{r['annotation']}\t{r['sense']}\t{r['pos']}\t{r['level']}\n")
            
    print(f"Successfully processed and wrote {len(records)} entries.")

if __name__ == "__main__":
    main()
