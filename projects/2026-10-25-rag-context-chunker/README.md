# RAG Context Chunker

A dependency-free Python command-line tool that splits plain-text documents into overlapping, JSON-ready chunks for RAG and LLM workflows.

## Requirements

- Python 3.10+
- No external packages

## Usage

```bash
cd projects/2026-10-25-rag-context-chunker
python3 context_chunker.py document.txt --max-chars 1200 --overlap-chars 160 --output chunks.json
```

The output contains an `id`, text, character count, and estimated token count for every chunk. Without `--output`, the JSON is written to standard output.

## Verification

```bash
cd projects/2026-10-25-rag-context-chunker
python3 -m unittest -v
```
