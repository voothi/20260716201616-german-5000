#!/usr/bin/env python3
"""
ZID: 20260716220354
Description: Unit tests for the german-5000 processing scripts.
             Imports modules from the sibling scripts directory.
"""

import sys
import os
import unittest
import importlib

# Add the sibling scripts directory to the python path
scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, scripts_dir)

class TestGermanScripts(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Dynamically import modules with numeric prefixes from scripts folder
        cls.m1 = importlib.import_module("1_convert_german_csv_to_tsv")
        cls.m2 = importlib.import_module("2_convert_german_by_frequency")

    def test_clean_german_lemma_m1(self):
        clean_fn = self.m1.clean_german_lemma
        self.assertEqual(clean_fn("der Mensch, -en"), "Mensch")
        self.assertEqual(clean_fn("das Jahr, -e"), "Jahr")
        self.assertEqual(clean_fn("andere (r, s)"), "andere")
        self.assertEqual(clean_fn("sein, ist, war, ist gewesen"), "sein, ist, war, ist gewesen")
        self.assertEqual(clean_fn("-jährig"), "-jährig")
        self.assertEqual(clean_fn("welch, -e, -er, -es"), "welch")
        self.assertEqual(clean_fn("die Frau, -en"), "Frau")
        self.assertEqual(clean_fn("der Tag, -e"), "Tag")
        self.assertEqual(clean_fn("das Buch, -̈er"), "Buch")
        self.assertEqual(clean_fn("die Mutter, -̈"), "Mutter")
        self.assertEqual(clean_fn("der Herr, -en"), "Herr")

    def test_clean_german_lemma_m2(self):
        clean_fn = self.m2.clean_german_lemma
        self.assertEqual(clean_fn("der Mensch, -en"), "Mensch")
        self.assertEqual(clean_fn("das Jahr, -e"), "Jahr")
        self.assertEqual(clean_fn("andere (r, s)"), "andere")
        self.assertEqual(clean_fn("sein, ist, war, ist gewesen"), "sein, ist, war, ist gewesen")
        self.assertEqual(clean_fn("-jährig"), "-jährig")
        self.assertEqual(clean_fn("welch, -e, -er, -es"), "welch")

    def test_german_sort_key(self):
        sort_key_fn = self.m1.german_sort_key
        
        # Test umlaut normalization
        self.assertEqual(sort_key_fn({"word": "Ägypten"})[0], "agypten")
        self.assertEqual(sort_key_fn({"word": "ähnlich"})[0], "ahnlich")
        self.assertEqual(sort_key_fn({"word": "übrig"})[0], "ubrig")
        self.assertEqual(sort_key_fn({"word": "groß"})[0], "gross")
        
        # Test sorting order comparison
        # "Ägypten" (agypten) should sort before "ah" (ah)
        self.assertLess(sort_key_fn({"word": "Ägypten"}), sort_key_fn({"word": "ah"}))
        # "Agentur" (agentur) should sort before "Ägypten" (agypten)
        self.assertLess(sort_key_fn({"word": "Agentur"}), sort_key_fn({"word": "Ägypten"}))

if __name__ == "__main__":
    unittest.main()
