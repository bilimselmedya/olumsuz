# IRT Model Prototype

> DİKKAT: Bu depo sürümünde eğitim ve kurulumla ilgili araçlar (ör. `train_irt.py`,
> `setup.*`, kurulum sunucusu vb.) kaldırıldı. README'de geçen bazı komutlar artık
> geçersiz olabilir. Gerekirse bu araçlar yeniden eklenebilir.

Bu klasör içinde basit bir Rasch/IRT (1PL) prototipi bulunmaktadır.

Hızlı kullanım:

1. Sanal çevre oluşturun ve bağımlılığı yükleyin:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Eğitimi çalıştırın:

```powershell
python train_irt.py
```

Sunucudan veriyle çalışma örneği:

```powershell
python train_irt.py --data-url "https://example.com/dataset.npz"
```

`dataset.npz` içinde `R` (matris) ve opsiyonel `theta`/`b` dizileri olabilir. Alternatif olarak JSON/CSV formatı da desteklenir.

HTTPS / kimlik doğrulama örnekleri:

- Bearer token ile:

```powershell
python train_irt.py --data-url "https://secure.example.com/dataset.npz" --auth-token "YOUR_TOKEN"
```

- Basic auth ile:

```powershell
python train_irt.py --data-url "https://secure.example.com/dataset.npz" --auth-user alice --auth-pass s3cr3t
```

- TLS doğrulamasını kapatma (test ortamı — güvensiz):

```powershell
python train_irt.py --data-url "https://self-signed.example/dataset.npz" --insecure
```

- İstemci sertifikası kullanma:

```powershell
python train_irt.py --data-url "https://secure.example.com/dataset.npz" --cert-path "path/to/cert.pem"
```

Alternatif — hazır bootstrap scriptleri

Windows (PowerShell):

```powershell
.\setup.ps1
```

Windows (cmd):

```bat
setup.bat
```

Linux / macOS / WSL:

```bash
./setup.sh
```

Kurulum sunucusunu arka planda başlatma ve görev olarak yükleme

- Arka planda başlatma (PowerShell):

```powershell
.\run_setup_server.ps1
```

- Scheduled Task (kullanıcı oturum açtığında başlat) oluşturma:

```powershell
.\install_setup_schtask.ps1 -TaskName "EgitimSetupServer"
```

Not: Görev oluşturma bazı Windows ortamlarında yönetici izni gerektirebilir.

Bu prototip, öğrenci-yetenek modelinin temel davranışını göstermek içindir. Gerçek verilerde
eksik cevaplar, zaman bağımlılığı, düzenli güncellemeler ve ölçeklendirme düşünülmelidir.
