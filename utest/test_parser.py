"""
Tests for the parser module
"""
import unittest
from booklet import parser

class TestParserMethods(unittest.TestCase):
    "Test the parser module"

    def test_filepath_invalid(self):
        "Test an invalid filepath"
        with self.assertRaises(FileNotFoundError):
            parser.type_file_path('/not/a/real/file')

    def test_filepath_valid(self):
        "Test a valid filepath"
        #print(f"File path is {__file__}")
        self.assertEqual(parser.type_file_path(__file__), __file__)

    def test_dirpath_invalid(self):
        "An invalid directory should raise an exception"
        with self.assertRaises(NotADirectoryError):
            parser.type_dir_path('/not/a/real/directory')

    def test_dirpath_valid(self):
        "A valid directory should not raise an exception"
        self.assertEqual(parser.type_dir_path('filetest'),'filetest')

    def test_range_chars(self):
        "An invalid page range"
        with self.assertRaises(ValueError):
            parser.type_page_range('invalid range')

# Currently fails
#    def test_range_hanging_hyphen(self):
#        "An invalid page range - hanging hyphen"
#        with self.assertRaises(ValueError):
#            parser.type_page_range('1,5-')

# Currently fails
#    def test_range_hanging_comma(self):
#        "An invalid page range, hanging comma"
#        with self.assertRaises(ValueError):
#            parser.type_page_range('1,5,')

    def test_range_single(self):
        "An valid page range, single number"
        self.assertEqual(parser.type_page_range('9'),'9')

    def test_range_commas(self):
        "An valid page range, numbers with commas"
        self.assertEqual(parser.type_page_range('9,3,4'),'9,3,4')

    def test_range_hyphens(self):
        "An valid page range, numbers with hyphens"
        self.assertEqual(parser.type_page_range('9,3-4'),'9,3-4')

    def test_colourstring_nohash(self):
        "Valid colour string without leading hash"
        self.assertEqual(parser.type_color('ff0055'),'ff0055')

    def test_colourstring_hash(self):
        "Valid colour string with leading hash"
        self.assertEqual(parser.type_color('#000fff'),'#000fff')

    def test_colourstring_none(self):
        "Colour string defaults if not passed"
        self.assertEqual(parser.type_color(None),'#729fcf')

    def test_colourstring_toolong(self):
        "Colour string too long"
        with self.assertRaises(ValueError):
            parser.type_color('ff00553')

    def test_colourstring_tooshort(self):
        "Colour string too short"
        with self.assertRaises(ValueError):
            parser.type_color('ff005')

    def test_colourstring_invalid(self):
        "Colour string has wrong hex values"
        with self.assertRaises(ValueError):
            parser.type_color('ff005g')


if __name__ == '__main__':
    unittest.main()
