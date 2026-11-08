# LLM PII Redactor

Bir metni LLM'e göndermeden önce sık karşılaşılan kişisel verileri yer tutucularla değiştiren, bağımlılıksız Python komut satırı aracı.

Desteklenen sinyaller:

- E-posta adresleri
- Yaygın telefon numarası biçimleri
- Uzun kart numarası benzeri sayı dizileri

Yer tutucular (`[EMAIL_1]`, `[PHONE_1]` gibi) aynı metin içindeki referansları takip etmeyi kolaylaştırır. Araç regex tabanlıdır; güvenlik garantisi değildir. Hassas içeriği paylaşmadan önce çıktıyı mutlaka gözden geçirin.

## Gereksinimler

- Python 3.10+
- Harici paket gerekmez

## Kullanım

```bash
cd projects/2026-11-08-llm-pii-redactor
python3 pii_redactor.py customer-note.txt --output sanitized.json
```

`sanitized.json`, temizlenmiş metni, tür bazında redaksiyon sayılarını ve toplam redaksiyon sayısını içerir. `--output` kullanılmadığında JSON standart çıktıya yazılır.

## Doğrulama

```bash
cd projects/2026-11-08-llm-pii-redactor
python3 -m unittest -v
```

Testler e-posta, telefon, kart numarası benzeri diziler, ardışık yer tutucular ve normal metnin korunmasını kapsar.
