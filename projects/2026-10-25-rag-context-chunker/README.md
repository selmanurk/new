# RAG Context Chunker

Düz metin belgelerini LLM/RAG akışlarına uygun, örtüşmeli JSON parçalara ayıran bağımlılıksız Python komut satırı aracı.

## Gereksinimler

- Python 3.10+
- Harici paket gerekmez

## Kullanım

```bash
cd projects/2026-10-25-rag-context-chunker
python3 context_chunker.py belge.txt --max-chars 1200 --overlap-chars 160 --output chunks.json
```

Çıktı, her parça için `id`, metin, karakter sayısı ve yaklaşık token tahmini içerir. `--output` kullanılmazsa JSON standart çıktıya yazılır.

## Doğrulama

```bash
cd projects/2026-10-25-rag-context-chunker
python3 -m unittest -v
```
