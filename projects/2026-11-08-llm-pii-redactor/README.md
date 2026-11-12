# LLM PII Redactor

A dependency-free Python command-line tool that replaces common personally identifiable information with placeholders before text is sent to an LLM.

Supported signals:

- Email addresses
- Common phone-number formats
- Long card-number-like digit sequences

Placeholders such as `[EMAIL_1]` and `[PHONE_1]` make references easy to follow within the same text. This is a regex-based utility, not a security guarantee; always review the output before sharing sensitive information.

## Requirements

- Python 3.10+
- No external packages

## Usage

```bash
cd projects/2026-11-08-llm-pii-redactor
python3 pii_redactor.py customer-note.txt --output sanitized.json
```

`sanitized.json` contains the redacted text, redaction counts by type, and the total redaction count. Without `--output`, the JSON is written to standard output.

## Verification

```bash
cd projects/2026-11-08-llm-pii-redactor
python3 -m unittest -v
```

The tests cover email addresses, phone numbers, card-number-like sequences, sequential placeholders, and preservation of ordinary text.
