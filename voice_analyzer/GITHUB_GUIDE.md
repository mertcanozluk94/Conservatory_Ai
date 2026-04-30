# 📤 conservatory.ai'yi GitHub'a Yükleme Rehberi

Bu rehber, projeni GitHub'a sıfırdan nasıl yükleyeceğini adım adım anlatır. Hiç Git/GitHub kullanmadıysan bile takip edebilirsin.

---

## 🎯 Hangi Yolu Seçmelisin?

İki yol var:

| Yol | Kim İçin? | Süre |
|-----|-----------|------|
| **A) GitHub Desktop** ⭐ | Komut satırından korkanlar | 10 dk |
| **B) Komut Satırı (Git)** | Geliştirici alışkanlığı olanlar | 15 dk |

> 💡 **Öneri**: İlk kez GitHub'a kod atıyorsan **GitHub Desktop**'u seç. Görsel arayüz çok daha kolay. Git komutlarını sonra istersen öğrenirsin.

---

# YOL A: GitHub Desktop ile (Önerilen) ⭐

## Adım 1: GitHub Hesabı Oluştur

1. **[github.com](https://github.com)** sitesine git
2. Sağ üstte **"Sign up"** butonuna tıkla
3. Email, şifre ve kullanıcı adı seç (kullanıcı adın kalıcı, dikkatli seç)
4. Email doğrulamasını yap
5. Ücretsiz "Free" planını seç

## Adım 2: GitHub Desktop'u İndir ve Kur

1. **[desktop.github.com](https://desktop.github.com)** sitesine git
2. **"Download for Windows"** (veya Mac) butonuna tıkla
3. İndirileni çalıştır → otomatik kurulum
4. Açılınca: **"Sign in to GitHub.com"** → hesabınla giriş yap
5. **"Configure Git"** ekranında ismini ve mailini gir → **Continue**
6. **"Finish"**

## Adım 3: Yeni Repository Oluştur

### GitHub.com'da:

1. **[github.com](https://github.com)**'a giriş yap
2. Sağ üstte **"+" simgesi** → **"New repository"**
3. Şu alanları doldur:

   | Alan | Ne Yazacaksın? |
   |------|----------------|
   | **Repository name** | `conservatory-ai` |
   | **Description** | `🎼 Conservatory-grade vocal analysis web app — discover your voice type, range, vibrato, and get personalized repertoire recommendations.` |
   | **Public/Private** | **Public** (LinkedIn'de paylaşacaksan public yap) |
   | **Add a README** | ❌ Boş bırak (zaten bizde var) |
   | **Add .gitignore** | ❌ Boş bırak (kendimiz ekleyeceğiz) |
   | **License** | **MIT License** seç |

4. **"Create repository"** butonuna tıkla

5. Şuna benzer bir sayfa göreceksin: `https://github.com/SENIN_KULLANICI_ADIN/conservatory-ai`

## Adım 4: .gitignore Dosyası Ekle (Önemli!)

`.gitignore` dosyası, GitHub'a **gitmemesi gereken** dosyaları belirler. Çok önemli — yoksa sanal ortamın (~500MB) gibi gereksiz şeyler yüklenir.

Proje klasöründe (yani `voice_analyzer/` klasörü içinde) **`.gitignore`** isimli yeni bir dosya oluştur. İçine şunu yapıştır:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
venv/
env/
ENV/
.venv

# Geçici dosyalar
uploads/*
!uploads/.gitkeep
reports/*
!reports/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Environment variables
.env
.env.local

# Logs
*.log
```

> 💡 **Windows'ta nokta ile başlayan dosya oluşturma**: Notepad'de `.gitignore` yazıp kaydederken "Tüm Dosyalar" seç ve adın sonuna nokta koyma (`.gitignore.txt` olmasın!). Veya VS Code kullan, kolay olur.

## Adım 5: Klasör Yapısını Hazırla

`uploads/` ve `reports/` klasörleri boş olduğu için Git onları görmez. İçlerine boş bir dosya koyalım:

1. `uploads/` klasörüne gir → boş bir dosya oluştur → adı: **`.gitkeep`**
2. `reports/` klasörüne gir → boş bir dosya oluştur → adı: **`.gitkeep`**

Bu dosyalar sadece klasörlerin var olduğunu Git'e söyler.

## Adım 6: GitHub Desktop ile Klonla

1. GitHub Desktop'u aç
2. **File** → **Clone repository...**
3. **GitHub.com** sekmesi → `conservatory-ai` repository'ni seç
4. **Local path**: Bilgisayarında nereye indirileceğini seç (örn. `Documents/GitHub/`)
5. **Clone** butonuna tıkla

> ⚠️ Bu, BOŞ bir klasör oluşturur. Dosyalarını **kendin** kopyalayacaksın bu klasöre.

## Adım 7: Dosyaları Klonlanan Klasöre Kopyala

1. Klonlanan boş `conservatory-ai` klasörünü aç
2. Mevcut `voice_analyzer/` klasöründeki **tüm dosyaları** (klasörler dahil) buraya kopyala:
   - `app.py`
   - `voice_analyzer.py`
   - `repertoire_guide.py`
   - `requirements.txt`
   - `README.md`
   - `DEPLOYMENT.md`
   - `LINKEDIN_POST.md`
   - `.gitignore`
   - `templates/` klasörü
   - `static/` klasörü (içindeki `chart.min.js` dahil)
   - `uploads/.gitkeep`
   - `reports/.gitkeep`

> ⚠️ **`venv/` klasörünü KOPYALAMA**! `.gitignore` zaten engelliyor ama yine de boşa yer kaplamasın.

## Adım 8: GitHub Desktop'ta Commit ve Push

1. GitHub Desktop'a geri dön
2. Sol tarafta tüm değişen dosyalar listelenir (yüzlerce dosya görmen normal)
3. Aşağıda **"Summary"** kutusuna yaz:
   ```
   Initial commit: conservatory.ai voice analysis app
   ```
4. **"Description"** boş bırakabilirsin
5. **"Commit to main"** butonuna tıkla (sol alt)
6. Commit yapıldıktan sonra üstte **"Push origin"** butonu çıkar → tıkla
7. Yükleme başlar (1-3 dakika)

## Adım 9: GitHub'da Kontrol Et

1. Tarayıcıda repo sayfana git: `https://github.com/SENIN_KULLANICI_ADIN/conservatory-ai`
2. Tüm dosyaları göreceksin
3. README.md otomatik render olacak — projenin tanıtım sayfası gibi 🎉

---

# YOL B: Komut Satırı ile

Eğer terminal kullanmaya alışkınsan:

## Adım 1: Git Kur

### Windows
**[git-scm.com](https://git-scm.com)** sitesinden indir → kur (varsayılan ayarlarla).

### Mac
```bash
brew install git
```

### Linux
```bash
sudo apt install git
```

## Adım 2: Git'e Kim Olduğunu Söyle

```bash
git config --global user.name "Senin Adın"
git config --global user.email "senin@email.com"
```

## Adım 3: GitHub'da Repo Oluştur

Yol A'daki **Adım 1-3**'ü yap.

## Adım 4: Yerelde Hazırla

```bash
# Proje klasörüne git
cd path/to/voice_analyzer

# .gitignore oluştur (Yol A Adım 4'teki içerikle)

# .gitkeep dosyalarını oluştur
touch uploads/.gitkeep reports/.gitkeep    # Mac/Linux
echo. > uploads/.gitkeep                    # Windows
echo. > reports/.gitkeep                    # Windows

# Git başlat
git init
git branch -M main

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: conservatory.ai voice analysis app"

# GitHub repository'ni ekle (URL'yi kendi repo'na göre değiştir)
git remote add origin https://github.com/SENIN_KULLANICI_ADIN/conservatory-ai.git

# Push et
git push -u origin main
```

İlk seferde GitHub kullanıcı adı + token isteyecek (şifre değil!). Token nasıl alınır:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → "repo" yetkisini seç → kopyala
3. Terminal'de şifre yerine bu token'ı yapıştır

---

# 🎨 Repository'yi Güzelleştir

Push ettikten sonra repo'nu daha çekici yapmak için:

## 1. Description ve Topics Ekle

Repo sayfanda sağ üstte **⚙️ ayar** ikonuna tıkla (About bölümünde):

### Description
```
🎼 Conservatory-grade vocal analysis web app — discover your voice type, range, vibrato, and get personalized repertoire recommendations.
```

### Website
Eğer deployment yaptıysan:
```
https://conservatory.ai
```

### Topics (Etiketler)
Tek tek ekle:
```
voice-analysis
music
singing
flask
python
praat
librosa
opera
vocal-coach
machine-learning
audio-processing
multilingual
```

## 2. Banner Görseli Ekle (Opsiyonel)

`/static/banner.png` gibi bir görsel ekleyip README'nin en başına şunu ekleyebilirsin:

```markdown
![conservatory.ai](static/banner.png)
```

Banner için fikir:
- Pitch contour grafiği görseli
- Editorial estetiği yansıtan bir kapak
- Canva ile 1280x640 boyutunda hızlıca yapılabilir

## 3. Releases Oluştur

İlk versiyonu işaretlemek için:
1. Repo sayfanda sağda **"Releases"** → **"Create a new release"**
2. **Tag**: `v1.0.0`
3. **Title**: `conservatory.ai v1.0.0 - Initial Release`
4. **Description**:
   ```
   🎉 First public release of conservatory.ai
   
   ## Features
   - 11 vocal Fach categories analysis
   - 15 language support
   - Live recording + file upload
   - Repertoire recommendations (classical & modern)
   - Vocal health indicators (jitter, shimmer, HNR)
   - Singer's formant detection
   ```
5. **Publish release**

## 4. Pin Repository

Profil sayfanda repo'nu öne çıkar:
1. GitHub profilinde sağda **"Customize your pins"**
2. `conservatory-ai`'yi seç → **Save pins**

---

# 📝 Sonradan Değişiklik Yaparsan

Projende değişiklik yapıp tekrar GitHub'a yüklemek için:

## GitHub Desktop ile
1. Dosyalarda değişiklik yap
2. GitHub Desktop'a git
3. Değişen dosyaları gör
4. Summary yaz (örn. "Added new language support")
5. **Commit to main** → **Push origin**

## Komut Satırı ile
```bash
git add .
git commit -m "Açıklama"
git push
```

---

# 🚨 Yaygın Hatalar

## "Repository contains files larger than 100MB"

Bir dosyan çok büyük (muhtemelen `venv/` klasörü). `.gitignore` doğru kurulmamış demektir. Çözüm:

```bash
git rm -r --cached venv
git commit -m "Remove venv folder"
git push
```

## "Permission denied (publickey)" veya kimlik doğrulama hatası

Personal Access Token kullanman gerekiyor (şifre değil). Yukarıdaki **Yol B Adım 4** kısmına bak.

## "fatal: not a git repository"

`git init` çalıştırmadan diğer komutları yazdın. Önce klasöre `cd` ile gir, sonra `git init` çalıştır.

## ZIP'inde gereksiz dosyalar var

`.gitignore` push'tan önce eklendiyse temizdir. Eğer sonradan eklediysen:

```bash
git rm -r --cached __pycache__
git rm -r --cached venv
git commit -m "Clean up gitignored files"
git push
```

---

# 🎁 Bonus: Star ve Fork Almak İçin

Kimsenin star vermediğini görmek üzücü ama strateji var:

1. **LinkedIn'de paylaş** (zaten yazımız hazır, `LINKEDIN_POST.md`)
2. **Reddit'te paylaş**:
   - r/Python
   - r/opera
   - r/singing
   - r/musictheory
3. **HackerNews "Show HN"** olarak paylaş
4. **Twitter/X**'te music tech topluluğunda paylaş
5. **dev.to** ve **Medium**'da blog yazısı yaz

İlk 10 star'ı dostlarından alabilirsin — utangaçlık etme, herkes böyle başlar.

---

# 🎉 Tebrikler!

Projen artık dünyaya açık. İnsanlar:
- ⭐ Star verebilir
- 🍴 Fork'layıp kendi versiyonlarını yapabilir
- 🐛 Issue açıp hata bildirebilir
- 🔧 Pull request gönderip katkıda bulunabilir

İyi şanslar! 🎼

---

<div align="center">

**conservatory.ai** — *now on GitHub* ✨

</div>
