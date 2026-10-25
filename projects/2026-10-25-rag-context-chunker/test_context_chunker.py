import unittest

from context_chunker import chunk_text, estimate_tokens


class ChunkTextTests(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(chunk_text("   "), [])

    def test_assigns_ids_and_respects_maximum(self):
        text = "Alpha one. Bravo two. Charlie three. Delta four."
        chunks = chunk_text(text, max_chars=24, overlap_chars=6)
        self.assertGreater(len(chunks), 1)
        self.assertEqual([chunk["id"] for chunk in chunks], list(range(1, len(chunks) + 1)))
        self.assertTrue(all(chunk["characters"] <= 24 for chunk in chunks))

    def test_preserves_all_sentence_content(self):
        text = "First fact. Second fact. Third fact."
        chunks = chunk_text(text, max_chars=21, overlap_chars=0)
        joined = " ".join(chunk["text"] for chunk in chunks)
        self.assertEqual(joined, text)

    def test_rejects_invalid_settings(self):
        with self.assertRaises(ValueError):
            chunk_text("Hello.", max_chars=10, overlap_chars=10)

    def test_token_estimate(self):
        self.assertEqual(estimate_tokens(""), 0)
        self.assertGreater(estimate_tokens("one two three"), 0)


if __name__ == "__main__":
    unittest.main()
