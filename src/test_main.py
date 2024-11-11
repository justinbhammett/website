import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_valid_header(self):
        markdown = "# This is a title"
        result = extract_title(markdown)
        self.assertEqual(result, "This is a title")
    def test_valid_header_with_extra_whitespace(self):
        markdown = "# This is a title with leading space"
        result = extract_title(markdown)
        self.assertEqual(result, "This is a title with leading space")
    def test_multiple_headers(self):
        markdown = """# First title\nSome content here.\n# Second title"""
        result = extract_title(markdown)
        self.assertEqual(result, "First title")
    def test_no_header(self):
        markdown = "This is a line without a header"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No header found")
    def test_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No header found")
    def test_header_in_middle(self):
        markdown = "Some content\n# Title in the middle\nMore content"
        result = extract_title(markdown)
        self.assertEqual(result, "Title in the middle")

if __name__ == "__main__":
    unittest.main()
