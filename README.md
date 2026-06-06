# Olumsuz — Eğitim İçgörü Prototipi


Kısa: Bu depo, Rasch/IRT tabanlı bir Eğitim İçgörüsü Motoru (EIM) prototipi içerir ve eğitim deneyimini kişiselleştirmek için temel araçlar sağlar.

Hızlı bağlantılar

- Yenilikler: [YENILIKLER.md](YENILIKLER.md)
- Güncelleme paketi: [UPDATE-2026-06-06.md](UPDATE-2026-06-06.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Politika dosyaları: [gizlilik-politikasi.md](gizlilik-politikasi.md), [guvenlik-politikasi.md](guvenlik-politikasi.md), [kvkk-aydinlatma.md](kvkk-aydinlatma.md), [hizmet-sartlari.md](hizmet-sartlari.md)

Hızlı başlangıç

1. Sanal çevre oluşturun ve bağımlılıkları yükleyin:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

1. Model eğitimi (örnek):

```powershell
python train_irt.py
```

Destek ve raporlama: [bilimharitasi@hotmail.com](mailto:bilimharitasi@hotmail.com)
