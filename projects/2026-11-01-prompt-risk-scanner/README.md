# Prompt Risk Scanner

LLM'e göndermeden önce güvenilmeyen metinlerde yaygın prompt-injection sinyallerini arayan, çevrimdışı ve bağımlılıksız bir Python CLI.

Araç şu sinyalleri işaretler:

- Önceki/sistem talimatlarını geçersiz kılma girişimleri
- Parola, token, API anahtarı veya kimlik bilgisi talepleri
- Ayrıcalıklı rol taklidi
- Veri ya da konuşma geçmişini dışarı gönderme istekleri

Bu bir güvenlik kararı değildir: sezgisel uyarılar üretir. Her zaman güvenilmeyen içeriği gözden geçirin ve araç yetkilerini en az ayrıcalıkla sınırlandırın.

## Gereksinimler

- Python 3.10+
- Harici paket gerekmez

## Kullanım

```bash
cd projects/2026-11-01-prompt-risk-scanner
python3 prompt_risk_scanner.py untrusted-prompt.txt --output risk-report.json
```

Çıktı JSON biçimindedir: risk seviyesi, bulgu sayısı, kural adı, kısa eşleşme ve karakter konumu içerir. `--output` verilmezse JSON standart çıktıya yazılır.

## Doğrulama

```bash
cd projects/2026-11-01-prompt-risk-scanner
python3 -m unittest -v
```

Testler zararsız metni, her bir temel risk sinyalini ve çoklu bulgulu yüksek-risk sınıflandırmasını kontrol eder.
