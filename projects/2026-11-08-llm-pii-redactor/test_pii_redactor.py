import unittest

from pii_redactor import redact


class PiiRedactorTests(unittest.TestCase):
    def test_redacts_email(self):
        result = redact("Contact ada@example.com for details.")
        self.assertEqual(result["redacted_text"], "Contact [EMAIL_1] for details.")
        self.assertEqual(result["counts"], {"EMAIL": 1})

    def test_redacts_phone_and_card(self):
        result = redact("Call +1 415 555 2671; card is 4111 1111 1111 1111.")
        self.assertIn("[PHONE_1]", result["redacted_text"])
        self.assertIn("[CARD_1]", result["redacted_text"])
        self.assertEqual(result["total_redactions"], 2)

    def test_uses_sequential_placeholders(self):
        result = redact("a@x.io and b@y.io")
        self.assertEqual(result["redacted_text"], "[EMAIL_1] and [EMAIL_2]")

    def test_keeps_non_sensitive_text(self):
        result = redact("Summarize this public product announcement.")
        self.assertEqual(result["total_redactions"], 0)
        self.assertEqual(result["redacted_text"], "Summarize this public product announcement.")


if __name__ == "__main__":
    unittest.main()
