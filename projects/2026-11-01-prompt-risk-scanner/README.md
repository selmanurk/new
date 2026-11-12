# Prompt Risk Scanner

An offline, dependency-free Python CLI that looks for common prompt-injection signals in untrusted text before it is sent to an LLM.

It flags:

- Attempts to override prior or system instructions
- Requests for passwords, tokens, API keys, or credentials
- Impersonation of privileged roles
- Requests to move data or conversation history outside the task

This is not a security decision engine—it produces heuristic warnings. I recommend reviewing all untrusted content and applying least-privilege tool access.

## Requirements

- Python 3.10+
- No external packages

## Usage

```bash
cd projects/2026-11-01-prompt-risk-scanner
python3 prompt_risk_scanner.py untrusted-prompt.txt --output risk-report.json
```

The JSON output includes the risk level, finding count, rule name, a short match excerpt, and character positions. Without `--output`, the JSON is written to standard output.

## Verification

```bash
cd projects/2026-11-01-prompt-risk-scanner
python3 -m unittest -v
```

The tests cover benign text, each core risk signal, and high-risk classification for multiple findings.
