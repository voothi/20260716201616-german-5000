# scripts/generate_html.py
import pandas as pd
import html
import argparse
import sys
import os

def generate_html(input_tsv, output_html, doc_title="Goethe German 5000", doc_subtitle=None, langs="en,ru", encoding="utf-8", newline="\n"):
    try:
        df = pd.read_csv(input_tsv, sep='\t')
        print(f"Shape of dataset '{input_tsv}':", df.shape)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    if not doc_subtitle:
        is_freq = "freq" in os.path.basename(input_tsv).lower() or "freq" in os.path.basename(output_html).lower()
        order_str = "organized by frequency" if is_freq else "organized alphabetically"
        doc_subtitle = f"The Goethe German 5000 is a core word list for learners of German, {order_str}, from A1 to C1 level."

    # Parse the target languages from the arguments
    target_langs = [l.strip().lower() for l in langs.split(',') if l.strip()]

    # Auto-detect if the English and Russian translation columns exist
    has_english = 'English' in df.columns
    has_russian = 'Russian' in df.columns

    # Dynamic CSS based on selected languages
    if 'en' in target_langs and 'ru' in target_langs:
        css_trans = """
    .trans-en { color: #195b98; margin-left: 3px; } /* Blue for English */
    .trans-ru { color: #b22222; margin-left: 3px; } /* Brick Brown for Russian */"""
    elif 'ru' in target_langs:
        css_trans = """
    .trans-ru { color: #195b98; margin-left: 3px; } /* Blue for Russian (standalone) */"""
    elif 'en' in target_langs:
        css_trans = """
    .trans-en { color: #195b98; margin-left: 3px; } /* Blue for English (standalone) */"""
    else:
        css_trans = ""

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {{
        size: A4;
        margin: 15mm 15mm 15mm 15mm;
        @bottom-left {{
            content: "© Goethe-Institut";
            font-size: 7pt;
            color: #666;
            font-family: "DejaVu Sans", "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
            margin-bottom: 5mm;
        }}
        @bottom-right {{
            content: counter(page) " / " counter(pages);
            font-size: 7pt;
            color: #666;
            font-family: "DejaVu Sans", "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
            margin-bottom: 5mm;
        }}
    }}
    body {{
        font-family: "DejaVu Sans", "Liberation Sans", "Helvetica Neue", Arial, sans-serif;
        font-size: 7.5pt;
        color: #333;
        line-height: 1.15;
        margin: 0;
        padding: 0;
    }}
    .header {{ margin-bottom: 3mm; }}
    .title {{
        color: #195b98; font-size: 26pt; font-weight: normal; margin: 0 0 8px 0; letter-spacing: -0.5px; font-family: "DejaVu Serif", "Liberation Serif", Georgia, serif;
    }}
    .subtitle {{ color: #555; font-size: 9pt; font-style: italic; margin: 0 0 10px 0; }}
    .divider {{ border-top: 1.5px solid #000; margin-bottom: 12px; }}
    .content {{ column-count: 3; column-gap: 20px; }}
    .entry {{ margin-bottom: 1.5px; page-break-inside: avoid; text-indent: -10px; padding-left: 10px; }}
    .word {{ color: #000; font-weight: bold; }}
    .pos {{ color: #555; font-style: italic; margin-left: 3px; }}
    .level {{ color: #777; margin-left: 3px; }}{css_trans}
</style>
</head>
<body>
    <div class="header">
        <div class="title">{html.escape(doc_title)}</div>
        <div class="subtitle">{html.escape(doc_subtitle)}</div>
        <div class="divider"></div>
    </div>
    <div class="content">
"""

    count = 0
    for _, row in df.iterrows():
        # Prefer Annotation over Word if available
        if 'Annotation' in row and pd.notna(row['Annotation']):
            word = str(row['Annotation'])
        elif 'Word' in row and pd.notna(row['Word']):
            word = str(row['Word'])
        else:
            word = ""
            
        pos = str(row['Part of Speech']) if 'Part of Speech' in row and pd.notna(row['Part of Speech']) else ""
        lvl = str(row['Level']) if 'Level' in row and pd.notna(row['Level']) else ""
        
        word_safe = html.escape(word)
        pos_safe = html.escape(pos)
        lvl_safe = html.escape(lvl)
        
        entry_html = f'<span class="word">{word_safe}</span> <span class="pos">{pos_safe}</span> <span class="level">{lvl_safe}</span>'
        
        # Append translations based on selected languages
        if has_english and 'en' in target_langs:
            trans_en = str(row['English']) if pd.notna(row['English']) else ""
            if trans_en and trans_en != 'nan':
                entry_html += f' <span class="trans-en">{html.escape(trans_en)}</span>'

        if has_russian and 'ru' in target_langs:
            trans_ru = str(row['Russian']) if pd.notna(row['Russian']) else ""
            if trans_ru and trans_ru != 'nan':
                entry_html += f' <span class="trans-ru">{html.escape(trans_ru)}</span>'
        
        html_content += f'        <div class="entry">{entry_html}</div>\n'
        count += 1

    html_content += """    </div>
</body>
</html>
"""

    # Normalize line endings to LF before writing
    html_content = html_content.replace("\r\n", "\n").replace("\r", "\n")

    with open(output_html, "w", encoding=encoding, newline=newline) as f:
        f.write(html_content)

    print(f"HTML generated successfully with {count} entries -> {output_html}")

def generate_all_html_files(base_dir=None, encoding="utf-8", newline="\n"):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    alpha_tsv_base = os.path.join(base_dir, "20260716200932-goethe-german-5000.de.tsv")
    alpha_tsv_ru = os.path.join(base_dir, "20260716200932-goethe-german-5000-ru.de.tsv")
    freq_tsv_base = os.path.join(base_dir, "20260716202200-goethe-german-5000-freq.de.tsv")
    freq_tsv_ru = os.path.join(base_dir, "20260716202200-goethe-german-5000-freq-ru.de.tsv")

    tasks = [
        # Alphabetical
        (alpha_tsv_base, os.path.join(base_dir, "20260716200932-goethe-german-5000.de.html"), ""),
        (alpha_tsv_base, os.path.join(base_dir, "20260716200932-goethe-german-5000-en.de.html"), "en"),
        (alpha_tsv_ru, os.path.join(base_dir, "20260716200932-goethe-german-5000-ru.de.html"), "ru"),
        (alpha_tsv_ru, os.path.join(base_dir, "20260716200932-goethe-german-5000-en-ru.de.html"), "en,ru"),
        # Frequency
        (freq_tsv_base, os.path.join(base_dir, "20260716202200-goethe-german-5000-freq.de.html"), ""),
        (freq_tsv_base, os.path.join(base_dir, "20260716202200-goethe-german-5000-freq-en.de.html"), "en"),
        (freq_tsv_ru, os.path.join(base_dir, "20260716202200-goethe-german-5000-freq-ru.de.html"), "ru"),
        (freq_tsv_ru, os.path.join(base_dir, "20260716202200-goethe-german-5000-freq-en-ru.de.html"), "en,ru"),
    ]

    for input_tsv, output_html, langs in tasks:
        if os.path.exists(input_tsv):
            generate_html(input_tsv, output_html, langs=langs, encoding=encoding, newline=newline)
        else:
            print(f"Warning: Input TSV not found: {input_tsv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Goethe HTML dictionary from TSV.")
    parser.add_argument("input_tsv", nargs="?", default=None, help="Input TSV file path")
    parser.add_argument("output_html", nargs="?", default=None, help="Output HTML file path")
    parser.add_argument("--title", default="Goethe German 5000", help="Title of the document")
    parser.add_argument("--subtitle", default=None, help="Subtitle of the document")
    parser.add_argument("--langs", default="en,ru", help="Comma-separated list of translations to include (e.g., 'ru' or 'en,ru'). Default: 'en,ru'")
    parser.add_argument("--encoding", default="utf-8", help="File output encoding (default: utf-8 without BOM)")
    parser.add_argument("--newline", default="\n", help="Line ending character (default: '\\n' / LF)")
    parser.add_argument("--all", action="store_true", help="Generate all 8 HTML files in project root")
    
    args = parser.parse_args()
    if args.all or (not args.input_tsv and not args.output_html):
        generate_all_html_files(encoding=args.encoding, newline=args.newline)
    elif args.input_tsv and args.output_html:
        generate_html(args.input_tsv, args.output_html, args.title, args.subtitle, args.langs, encoding=args.encoding, newline=args.newline)
    else:
        parser.print_help()