# German 5000 Wordlist Curation & Caching Pipeline

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/voothi/20260716201616-german-5000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AnkiWeb Deck](https://img.shields.io/badge/AnkiWeb_Deck-38922074-blue.svg?logo=anki)](https://ankiweb.net/shared/info/38922074)
[![AnkiWeb Add-on](https://img.shields.io/badge/AnkiWeb_Add--on-1967530655-blue.svg?logo=anki)](https://ankiweb.net/shared/info/1967530655)

A specialized data curation project designed to produce highly accurate, clean, and verified TSV lists for the Goethe Institute German 5000 vocabulary database. This repository packages the sanitized datasets along with a suite of Python scripts to manage and verify the data pipeline.

The official lists are based on the [Goethe-Institut Wordlists](https://www.goethe.de/).

## Table of Contents
- [Project Goal](#project-goal)
- [Curation Workflow & History](#curation-workflow--history)
- [Project Structure](#project-structure)
- [Data Modeling & Format Patterns](#data-modeling--format-patterns)
  - [1. Clean Lemma Extraction Pattern](#1-clean-lemma-extraction-pattern)
  - [2. Original Word Annotation Pattern](#2-original-word-annotation-pattern)
- [Pipelines & Scripts Details](#pipelines--scripts-details)
- [Usage](#usage)
  - [Running the Alphabetical Conversion](#running-the-alphabetical-conversion)
  - [Running the Frequency Conversion](#running-the-frequency-conversion)
  - [Running the Unit Tests](#running-the-unit-tests)
- [License](#license)

---

## Project Goal
The primary objective of this project is to compile, sanitize, and verify the Goethe German 5000 vocabulary lists to a high standard of accuracy in both alphabetical and frequency orders. This includes extracting clean, article-free base lemmas (e.g. `Mensch` from `der Mensch, -en`), isolating inflectional parentheticals (e.g. `andere (r, s)` $\rightarrow$ `andere`), keeping verb conjugations comma-separated (e.g. `sein, ist, war, ist gewesen`), and combining multiple parts of speech into unified columns. The processing scripts are packaged with the data to support future adjustments and reproducibility.

The original vocabulary data was exported from the [German 5000 Frequency Words Audio + Conjugations + Goethe V2](https://ankiweb.net/shared/info/38922074) Anki deck using the [Copy notes to clipboard](https://ankiweb.net/shared/info/1967530655) AnkiWeb add-on.

[Return to Top](#german-5000-wordlist-curation--caching-pipeline)

## Curation Workflow & History
The curation and verification process evolved through the following stages:

1.  **Initial Schema Review:** Analyzing the 27-column, semicolon-separated raw CSV files containing word definitions, pronunciations, level metadata, and multiple parts of speech.
2.  **Lemma & Annotation Design:** Mitigating silent lookup failures in `kardenwort` (caused by noun articles and plural suffixes) by separating base lemmas for matching and moving the original strings into the `Annotation` column.
3.  **Refined German Sorting:** Implementing German dictionary sorting rules (DIN 5007 Variant 1) to treat umlauts as their base characters, preventing them from being pushed to the end of the alphabetical list.
4.  **Frequency Preservation:** Running a secondary pipeline to convert the frequency-ordered dataset without sorting it.

## Project Structure
```text
U:\voothi\20260716201616-german-5000\
├── scripts/
├── tests/
├── .gitattributes
├── .gitignore
├── 20260716200932-goethe-german-5000-ru.de.html      # Alphabetical HTML (with Russian)
├── 20260716200932-goethe-german-5000-ru.de.pdf       # Alphabetical PDF (with Russian)
├── 20260716200932-goethe-german-5000-ru.de.tsv       # Alphabetical TSV (with Russian)
├── 20260716200932-goethe-german-5000.de.csv          # Original source CSV
├── 20260716200932-goethe-german-5000.de.html         # Alphabetical HTML
├── 20260716200932-goethe-german-5000.de.pdf          # Alphabetical PDF
├── 20260716200932-goethe-german-5000.de.tsv          # Alphabetical TSV
├── 20260716201616-german-5000.code-workspace         # VS Code Workspace Configuration
├── 20260716202200-goethe-german-5000-freq-ru.de.html # Frequency-ordered HTML (with Russian)
├── 20260716202200-goethe-german-5000-freq-ru.de.pdf  # Frequency-ordered PDF (with Russian)
├── 20260716202200-goethe-german-5000-freq-ru.de.tsv  # Frequency-ordered TSV (with Russian)
├── 20260716202200-goethe-german-5000-freq.de.csv     # Original source CSV (Frequency)
├── 20260716202200-goethe-german-5000-freq.de.html    # Frequency-ordered HTML
├── 20260716202200-goethe-german-5000-freq.de.pdf     # Frequency-ordered PDF
├── 20260716202200-goethe-german-5000-freq.de.tsv     # Frequency-ordered TSV
├── German 5000 Frequency Words Audio + Conjugations + Goethe V2 - AnkiWeb.url
├── LICENSE
├── README.md
├── update_names.py
└── update_trees.py
```

[Return to Top](#german-5000-wordlist-curation--caching-pipeline)

## Data Modeling & Format Patterns

The pipeline maps raw parts of speech and level notations from the source CSV files into a 5-column target TSV with the following headers:
- `Word`: The clean lowercase dictionary headword (excluding articles, plural suffixes, and parenthetical inflections).
- `Annotation`: The original raw German string, preserving articles, plural forms, and details for human reference.
- `Sense`: The homonym sense index number (if applicable).
- `Part of Speech`: Combined parts of speech.
- `Level`: The word's CEFR level.

### 1. Clean Lemma Extraction Pattern
To avoid silent lookup failures when `kardenwort` evaluates lemmatized words against the dictionary:
*   **Articles**: Prefixes like `der `, `die `, and `das ` are stripped (e.g. `der Mensch` $\rightarrow$ `Mensch`). Standalone articles are kept.
*   **Declension Suffixes**: Suffixes starting with a hyphen in comma-separated parts (e.g. `-en` in `der Mensch, -en`) are skipped.
*   **Inflectional Parentheticals**: Suffix inflections (e.g. `andere (r, s)` $\rightarrow$ `andere`) are removed.

### 2. Original Word Annotation Pattern
To ensure no grammatical information is lost for human readers:
*   The raw string (including articles, plural suffixes, and parentheticals) is copied to the `Annotation` column.

> [!NOTE]
> Verbs with comma-separated inflections (e.g., `sein, ist, war, ist gewesen`) are preserved as comma-separated values in the `Word` column. `kardenwort` natively splits them on comma, indexing all listed inflected forms under the same level (`A1`).

[Return to Top](#german-5000-wordlist-curation--caching-pipeline)

## Pipelines & Scripts Details

1.  **`1_convert_german_csv_to_tsv.py`:**
    *   *Input:* `20260716200932-goethe-german-5000.de.csv`
    *   *Operation:* Normalizes nouns/inflections, merges Parts of Speech, sorts alphabetically using German dictionary rules (DIN 5007 Variant 1) treating umlauts as base vowels, and writes to `20260716200932-goethe-german-5000.de.tsv` and `kardenwort` data folder.
2.  **`2_convert_german_by_frequency.py`:**
    *   *Input:* `20260716202200-goethe-german-5000-freq.de.csv`
    *   *Operation:* Normalizes nouns/inflections, merges Parts of Speech, preserves the original frequency order as is (unsorted), and writes to `20260716202200-goethe-german-5000-freq.de.tsv` and `kardenwort` data folder.

[Return to Top](#german-5000-wordlist-curation--caching-pipeline)

## Usage

### Running the Alphabetical Conversion
Execute the script from the terminal to recreate the German-sorted alphabetical TSV file:
```powershell
python U:\voothi\20260716201616-german-5000\scripts\1_convert_german_csv_to_tsv.py
```

### Running the Frequency Conversion
Execute the script from the terminal to recreate the unsorted frequency-ordered TSV file:
```powershell
python U:\voothi\20260716201616-german-5000\scripts\2_convert_german_by_frequency.py
```

### Running the Unit Tests
Execute the unit test suite from the terminal to verify clean lemma extraction and sorting rules:
```powershell
python U:\voothi\20260716201616-german-5000\tests\test_scripts.py
```

[Return to Top](#german-5000-wordlist-curation--caching-pipeline)

## License
MIT License. See `LICENSE` for details.

[Return to Top](#german-5000-wordlist-curation--caching-pipeline)

## Generating PDF from TSV

You can provide the AI with the TSV file and use the following prompt to trigger the exact same PDF generation process:

> **Prompt:** "Please read the attached TSV file containing the dictionary list. Using your Python execution environment, generate an HTML file and convert it to a 3-column A4 PDF using `pandas` and `weasyprint`. Format the 'Word' (or 'Annotation') in bold black, the 'Part of Speech' and 'Level' in grey italics, and append the 'Russian' translation from the last column in blue. Include page numbers and copyright text at the bottom. Do not let individual entries break across pages or columns."

There is also a Python script `scripts/tsv_to_pdf.py` available if you want to run this locally in your own environment.

[Return to Top](#german-5000-wordlist-curation--caching-pipeline)

## Generating HTML from TSV

The `scripts/generate_html.py` script was generated using Gemini 3.1 Pro Extended with the following prompts. Along with the prompts, the corresponding pairs of reference files (e.g., `20260716200932-goethe-german-5000-ru.de.pdf` and `20260716200932-goethe-german-5000-ru.de.tsv`) were attached as context:

```text
20260722113359 Generate exact HTML from the TSV file similar to the attached PDF. Output ready full HTML file.

// scripts/generate_html.py
...
```

```text
20260722114600 Now do this one, name it 20260716200932-goethe-german-5000-ru.de.html
```

```text
20260722115656 Update the script if necessary. And take me out.
// scripts/generate_html.py
```
