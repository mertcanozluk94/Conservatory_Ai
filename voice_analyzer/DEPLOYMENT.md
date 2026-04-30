# 🚀 conservatory.ai — Deployment Rehberi

Bu rehber, conservatory.ai'yi internete nasıl yayınlayacağını adım adım anlatır. Bütçenize ve teknik bilginize göre **4 farklı seçenek** sunuyoruz.

---

## 📋 Hızlı Karar Rehberi

| Senaryo | Önerilen | Aylık Maliyet |
|---------|----------|---------------|
| **Hızlı test, küçük kullanıcı** | Render.com (Free) | $0 |
| **Profesyonel başlangıç** | Railway.app | $5-10 |
| **Kontrollü ve ucuz** | DigitalOcean Droplet | $6 |
| **Yüksek trafik, ölçeklenebilir** | AWS EC2 + CloudFront | $15+ |

> 💡 **Öneri**: Yeni başlıyorsan **Railway.app** ile başla. Hem ucuz hem dert etmiyorsun, otomatik HTTPS ve domain yönetimi var.

---

## 🔧 Production İçin Hazırlık (Hepsi İçin Geçerli)

Yayınlamadan önce projende şu değişiklikleri yapman gerek:

### 1. `requirements.txt`'e gunicorn ekle

```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

### 2. `Procfile` oluştur (kök dizinde)

```
web: gunicorn app:app --workers 2 --threads 4 --timeout 120
```

> ⚠️ **Önemli**: Ses analizi 10-30 saniye sürebilir, `--timeout 120` şart.

### 3. `app.py`'i production için güncelle

```python
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
    # Production'da debug=False olmalı!
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

### 4. `.gitignore` oluştur

```
venv/
__pycache__/
*.pyc
uploads/*
!uploads/.gitkeep
reports/*
!reports/.gitkeep
.env
.DS_Store
```

### 5. `runtime.txt` (Python sürümü için)

```
python-3.11.7
```

---

## 🎯 Seçenek 1: Render.com (ÜCRETSIZ — Önerilen Başlangıç)

Render'ın ücretsiz katmanı conservatory.ai için yeterli. Tek dezavantajı: 15 dakika trafik gelmezse uyumaya geçer (ilk istek 30 saniye sürer).

### Adımlar

**1.** [github.com](https://github.com)'da bir hesap aç ve projeni push et:

```bash
cd voice_analyzer
git init
git add .
git commit -m "İlk commit"
git remote add origin https://github.com/KULLANICI_ADIN/conservatory-ai.git
git push -u origin main
```

**2.** [render.com](https://render.com)'a git, GitHub ile giriş yap

**3.** Dashboard → **New +** → **Web Service**

**4.** Repository'yi seç: `conservatory-ai`

**5.** Ayarları yap:
- **Name**: `conservatory-ai`
- **Region**: Frankfurt (Türkiye'ye en yakın)
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  apt-get update && apt-get install -y ffmpeg libsndfile1 && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn app:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT
  ```
- **Plan**: Free

**6.** **Create Web Service** → 5-10 dakika içinde hazır

**7.** Sana `https://conservatory-ai.onrender.com` gibi bir URL verir.

### Custom Domain (conservatory.ai) Ekleme

1. Render dashboard → Web Service → **Settings** → **Custom Domains**
2. **Add Custom Domain** → `conservatory.ai` yaz
3. Render sana DNS kayıtları verir (A record + CNAME)
4. Domain sağlayıcına git (Namecheap, GoDaddy, vb.) → DNS panel
5. Verilen kayıtları ekle
6. 1-24 saat içinde aktif olur, HTTPS otomatik

---

## ⭐ Seçenek 2: Railway.app (En Kolay — $5/ay)

Render'a göre daha hızlı, uyumaya geçmez. Aylık $5 kredi yeterli.

### Adımlar

**1.** Projeyi GitHub'a push et (yukarıdaki gibi)

**2.** [railway.app](https://railway.app)'e git, GitHub ile giriş yap

**3.** **New Project** → **Deploy from GitHub repo** → `conservatory-ai`

**4.** Otomatik deploy başlar — Railway nixpacks ile her şeyi halleder

**5.** Settings → **Variables** → şunu ekle:
```
PYTHON_VERSION=3.11
NIXPACKS_APT_PKGS=ffmpeg,libsndfile1
```

**6.** Settings → **Networking** → **Generate Domain** → ücretsiz `.up.railway.app` URL'i

**7.** Custom domain için: **Custom Domain** → `conservatory.ai` → DNS yönergelerini takip et

> 💡 İlk $5 kredi ücretsiz. 100k istek/ay ortalama yeterli.

---

## 🛠️ Seçenek 3: DigitalOcean Droplet ($6/ay — En Kontrollü)

Tam kontrol istiyorsan ve Linux komut satırından korkmuyorsan en ucuz çözüm.

### Adım 1: Droplet Oluştur

1. [digitalocean.com](https://digitalocean.com) → **Create** → **Droplet**
2. **Image**: Ubuntu 22.04 LTS
3. **Plan**: Basic — $6/ay (1GB RAM, 25GB SSD)
4. **Region**: Frankfurt
5. **Authentication**: SSH key (önerilir) veya password
6. **Create Droplet**

### Adım 2: Sunucuya Bağlan

```bash
ssh root@SUNUCU_IP_ADRESI
```

### Adım 3: Sistem Hazırlığı

```bash
# Sistemi güncelle
apt update && apt upgrade -y

# Gerekli paketler
apt install -y python3-pip python3-venv nginx ffmpeg libsndfile1 git certbot python3-certbot-nginx

# Yeni kullanıcı (root ile çalışmamak için)
adduser conservatory
usermod -aG sudo conservatory
su - conservatory
```

### Adım 4: Projeyi Yükle

```bash
cd ~
git clone https://github.com/KULLANICI_ADIN/conservatory-ai.git
cd conservatory-ai

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Adım 5: systemd Service

```bash
sudo nano /etc/systemd/system/conservatory.service
```

İçerik:
```ini
[Unit]
Description=conservatory.ai Gunicorn
After=network.target

[Service]
User=conservatory
Group=www-data
WorkingDirectory=/home/conservatory/conservatory-ai
Environment="PATH=/home/conservatory/conservatory-ai/venv/bin"
ExecStart=/home/conservatory/conservatory-ai/venv/bin/gunicorn \
    --workers 2 --threads 4 --timeout 120 \
    --bind unix:conservatory.sock \
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start conservatory
sudo systemctl enable conservatory
sudo systemctl status conservatory  # Çalışıyor mu kontrol
```

### Adım 6: Nginx Yapılandırması

```bash
sudo nano /etc/nginx/sites-available/conservatory
```

İçerik:
```nginx
server {
    listen 80;
    server_name conservatory.ai www.conservatory.ai;

    client_max_body_size 60M;  # Ses dosyaları için

    location / {
        proxy_pass http://unix:/home/conservatory/conservatory-ai/conservatory.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Uzun analiz timeout'ları için
        proxy_read_timeout 180s;
        proxy_connect_timeout 180s;
        proxy_send_timeout 180s;
    }

    location /static {
        alias /home/conservatory/conservatory-ai/static;
        expires 30d;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/conservatory /etc/nginx/sites-enabled/
sudo nginx -t  # Test
sudo systemctl restart nginx
```

### Adım 7: HTTPS (Let's Encrypt)

```bash
sudo certbot --nginx -d conservatory.ai -d www.conservatory.ai
```

Otomatik yenileme:
```bash
sudo certbot renew --dry-run
```

### Adım 8: DNS Yapılandırması

Domain sağlayıcında:
- **A record**: `conservatory.ai` → SUNUCU_IP_ADRESI
- **A record**: `www.conservatory.ai` → SUNUCU_IP_ADRESI

---

## 🌐 Domain Satın Alma (conservatory.ai)

`.ai` domain'leri özel — biraz pahalı:

| Sağlayıcı | Yıllık Maliyet | Notlar |
|-----------|---------------|--------|
| **Namecheap** | ~$70 | Kullanıcı dostu |
| **Porkbun** | ~$55 | En ucuz seçenek |
| **101domain** | ~$100 | Daha eski sağlayıcı |
| **Cloudflare** | ~$70 | Yıllık ücret + CDN dahil |

> 💡 Sadece test için `.ai` yerine **conservatoryai.com** veya **myconservatory.app** gibi alternatifleri düşünebilirsin (~$10/yıl).

### Domain Aldıktan Sonra

1. Domain sağlayıcı panelinden **Nameservers** veya **DNS Records** bölümüne git
2. Yukarıdaki rehberlerdeki DNS kayıtlarını ekle
3. Propagasyon 1-24 saat sürebilir — [whatsmydns.net](https://whatsmydns.net) ile kontrol edebilirsin

---

## 🔒 Güvenlik Kontrol Listesi

Yayına almadan önce mutlaka yap:

- [ ] `app.py`'de `debug=False`
- [ ] `.env` veya environment variable'lar git'e gitmiyor
- [ ] HTTPS aktif (`https://`)
- [ ] Rate limiting eklendi (Flask-Limiter — opsiyonel)
- [ ] `uploads/` ve `reports/` klasörleri otomatik temizleniyor
- [ ] Maximum dosya boyutu (`MAX_CONTENT_LENGTH = 50MB`) korunuyor
- [ ] Allowed file extensions kontrol ediliyor
- [ ] Hata mesajları detay sızdırmıyor (production)

### Rate Limiting Eklemek (Önerilir)

```bash
pip install Flask-Limiter
```

`app.py`'in başına:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per hour")  # IP başına saatte 10 analiz
def analyze():
    ...
```

---

## 📊 Disk ve Trafik Yönetimi

`uploads/` ve `reports/` klasörleri zamanla şişer. `app.py`'e otomatik temizlik ekle:

```python
import time
from threading import Thread

def cleanup_old_files():
    """24 saatten eski raporları sil"""
    while True:
        try:
            now = time.time()
            for folder in [app.config['UPLOAD_FOLDER'], app.config['REPORTS_FOLDER']]:
                for filename in os.listdir(folder):
                    filepath = os.path.join(folder, filename)
                    if os.path.isfile(filepath):
                        if now - os.path.getmtime(filepath) > 86400:  # 24 saat
                            os.remove(filepath)
        except:
            pass
        time.sleep(3600)  # Saatte bir çalış

# Uygulama başlarken background thread başlat
cleanup_thread = Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()
```

---

## 🐛 Sorun Giderme

### "ffmpeg not found" hatası
- Render: Build command'a `apt-get install -y ffmpeg` ekle
- Railway: `NIXPACKS_APT_PKGS=ffmpeg,libsndfile1` env var
- DigitalOcean: `sudo apt install ffmpeg`

### "Memory limit exceeded"
- Worker sayısını azalt (`--workers 1`)
- Plan'ını yükselt (en az 1GB RAM önerilir)

### Upload 413 hatası
- Nginx: `client_max_body_size 60M;` ekle
- Cloudflare: Plan upload limit'ini kontrol et

### "Application failed to respond"
- Timeout artır: `--timeout 180`
- Logları kontrol et: `journalctl -u conservatory -n 50`

### HTTPS sertifika hatası
```bash
sudo certbot renew
sudo systemctl restart nginx
```

---

## 📈 Sonraki Adımlar

Yayına aldıktan sonra:

- 📊 **Analytics**: [Plausible](https://plausible.io) veya [Umami](https://umami.is) (privacy-first)
- 🐛 **Hata takibi**: [Sentry](https://sentry.io) ücretsiz katmanı
- ⚡ **CDN**: Cloudflare (ücretsiz) — global hız + DDoS koruması
- 📧 **E-posta bildirimleri**: SendGrid / Mailgun (analizi e-postayla göndermek için)
- 💾 **Veritabanı**: Kullanıcı hesapları için PostgreSQL (Supabase ücretsiz)

---

## 🎯 Çıkış Yaparken

İlk yayında trafik az olur. Stres yapma. 

İyi şanslar! 🎼

> *"Music is the universal language of mankind."* — Henry Wadsworth Longfellow

---

<div align="center">

**conservatory.ai** — *Made with ♪*

</div>
