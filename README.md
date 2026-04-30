<div align="center">

# 🎼 conservatory.ai

### *Discover the anatomy of your voice — at conservatory standards*

[![Python](https://img.shields.io/badge/Python-3.10+-c4923a?style=flat-square)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-c4923a?style=flat-square)](https://flask.palletsprojects.com)
[![Praat](https://img.shields.io/badge/Praat-parselmouth-c4923a?style=flat-square)](https://parselmouth.readthedocs.io)
[![Languages](https://img.shields.io/badge/Languages-15-c4923a?style=flat-square)](#-15-language-support)

*"La voce è l'anima fatta suono."*  
*(The voice is the soul made sound.)*

</div>

---

## ✨ What Is This?

**conservatory.ai** is a web application that scientifically analyzes your singing voice. It combines the Praat acoustic analysis engine with modern Python libraries to give you the kind of detailed feedback a professional voice coach might provide:

- 🎭 **What's your voice type?** (across 11 classical categories)
- 💪 **How healthy is your voice?** (jitter, shimmer, HNR analysis)
- 🎵 **What music suits your voice?** (both classical and modern repertoire)
- 📚 **What should you start practicing?** (tailored recommendations)

All from a single voice recording — analyzed, interpreted, and visualized.

---

## 🎯 Features

### Scientific Analysis

| Parameter | What It Measures |
|-----------|------------------|
| **Vocal Range** | Lowest and highest notes — in octaves |
| **Tessitura** | The comfortable zone where your voice naturally sits |
| **Fach Classification** | 11 classical voice categories (Coloratura to Bass) |
| **Passaggio** | Primo/secondo register transitions |
| **Vibrato** | Rate (Hz) + extent (semitones) + quality |
| **Jitter & Shimmer** | Vocal fold health using Praat standards |
| **HNR** | Harmonics-to-Noise Ratio — voice clarity |
| **Formants** | F1, F2, F3 + Singer's Formant detection |
| **Dynamic Range** | dB difference from pp to ff |
| **Pitch Contour** | Time/frequency visualization |

### Repertoire Guide 🎵

After each analysis, you get personalized recommendations for your voice type:

- 🎭 **Classical repertoire**: Which opera arias, lieder, and oratorios suit you?
- 🎤 **Modern repertoire**: Which artists in pop, jazz, or musicals can serve as references?
- ⚠️ **What to avoid**: Styles that don't suit your voice
- ✦ **Training tips**: Technical advice tailored to your voice type

### Instructor Assessment

A three-column professional report — from a real vocal coach's perspective:

- ↗ **Strengths** — what shines about your voice
- ○ **Practice Recommendations** — areas to develop
- ! **Points of Caution** — vocal health warnings

### 15 Language Support 🌍

🇹🇷 Türkçe · 🇬🇧 English · 🇨🇳 中文 · 🇮🇳 हिन्दी · 🇪🇸 Español · 🇸🇦 العربية · 🇫🇷 Français · 🇧🇩 বাংলা · 🇵🇹 Português · 🇷🇺 Русский · 🇵🇰 اردو · 🇮🇩 Indonesia · 🇩🇪 Deutsch · 🇯🇵 日本語 · 🇰🇷 한국어

Includes RTL support (Arabic, Urdu) and optimized fonts for Asian scripts.

---

# 🚀 Installation Guide

> **No coding experience? No problem.** Just follow these steps carefully and you'll have it running in 10-15 minutes.

## What You'll Need

- A computer running **Windows 10/11, macOS, or Linux**
- Internet connection
- About **500 MB** of free disk space
- 10-15 minutes

## Three Things to Install

You'll install three things in order:

1. **Python** (the programming language)
2. **FFmpeg** (audio processor — required for live recording!)
3. **conservatory.ai** itself

Let's go!

---

## Step 1: Install Python

### 🪟 Windows

1. Go to **[python.org/downloads](https://www.python.org/downloads/)**
2. Click the big yellow **"Download Python 3.11.x"** button
3. Run the installer
4. ⚠️ **VERY IMPORTANT**: Check the box **"Add Python to PATH"** at the bottom of the installer
5. Click **"Install Now"**
6. Wait for it to finish, then click **Close**

**Verify it works:**

Press `Windows + R`, type `cmd`, press Enter. In the black window, type:
```
python --version
```

You should see `Python 3.11.7` (or similar). If you see "not recognized", you missed the PATH checkbox — uninstall Python and reinstall.

### 🍎 Mac

Open **Terminal** (`Cmd+Space`, type "terminal"). If you have Homebrew:
```bash
brew install python@3.11
```

If you don't have Homebrew, install it first from **[brew.sh](https://brew.sh)**.

**Verify:**
```bash
python3 --version
```

### 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

## Step 2: Install FFmpeg ⭐ (CRITICAL — don't skip!)

FFmpeg is a free tool that processes audio files. **conservatory.ai needs it for two reasons**:

1. **Live recording from your browser uses WebM format** — Praat (the analysis engine) only reads WAV. FFmpeg converts WebM to WAV automatically.
2. **MP3, M4A, OGG files all need converting** — same reason.

Without FFmpeg, only `.wav` files will work, and live browser recording will fail with errors like *"Not an audio file"*.

### 🪟 Windows — The Easy Way (Recommended)

Open **PowerShell** (search "PowerShell" in Start menu) and run:

```powershell
winget install Gyan.FFmpeg
```

That's it! winget downloads and installs FFmpeg automatically. ✅

> **Don't have winget?** It comes built-in with Windows 10/11. If it's missing, run Windows Update first.

### 🪟 Windows — Manual Installation (If winget fails)

1. Go to **[gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)**
2. Scroll to "release builds"
3. Download **`ffmpeg-release-essentials.zip`**
4. Right-click the ZIP → **Extract All** → choose `C:\`
5. Rename the extracted folder to just **`ffmpeg`**  
   You should now have `C:\ffmpeg\bin\ffmpeg.exe`
6. Add to PATH:
   - Press `Windows`, type "environment variables"
   - Click **"Edit the system environment variables"**
   - Click **"Environment Variables..."** button
   - Under "User variables", select **`Path`** → click **Edit** → click **New**
   - Type: `C:\ffmpeg\bin`
   - Click **OK** three times to close all dialogs

### 🍎 Mac

```bash
brew install ffmpeg
```

### 🐧 Linux

```bash
sudo apt install ffmpeg libsndfile1
```

### ⚠️ Verify FFmpeg Installation

**This step is critical.** Close ALL terminal/PowerShell windows, then open a new one and run:

```bash
ffmpeg -version
```

You should see something like:
```
ffmpeg version 6.1-essentials_build ...
```

✅ If you see this, FFmpeg is ready.

❌ If you see "not recognized" or "command not found":
- Make sure you closed and reopened the terminal
- Try restarting your computer
- Verify the PATH was set correctly (Step 2)

---

## Step 3: Get conservatory.ai

### Option A: Download ZIP (Easier for beginners)

1. Download the project as a `.zip` file
2. Extract it somewhere you'll remember (e.g., `Documents/conservatory-ai`)

### Option B: Clone with Git (For developers)

```bash
git clone https://github.com/YOUR_USERNAME/conservatory-ai.git
```

---

## Step 4: Install Dependencies

Open a terminal/PowerShell. Navigate to the project folder:

```bash
# Windows example:
cd C:\Users\YourName\Documents\conservatory-ai\voice_analyzer

# Mac/Linux example:
cd ~/Documents/conservatory-ai/voice_analyzer
```

### Create a Virtual Environment (Recommended)

A virtual environment isolates this project's libraries from the rest of your system.

```bash
# Create it
python -m venv venv

# Activate it
# 🪟 Windows:
venv\Scripts\activate

# 🍎🐧 Mac/Linux:
source venv/bin/activate
```

After activation, you'll see `(venv)` at the start of your terminal line. That means it worked. ✅

### Install Required Libraries

```bash
pip install -r requirements.txt
```

This installs Flask, librosa, parselmouth, and dependencies. Takes 2-5 minutes.

> 💡 **You might see warnings** about other packages on your system (torch, transformers, etc.). These are unrelated to conservatory.ai and can be ignored.

---

## Step 5: Run the App

Still in the `voice_analyzer` folder with venv active:

```bash
python app.py
```

You'll see this banner:
```
============================================================
conservatory.ai - Voice Analysis Server
============================================================
✓ FFmpeg detected: ffmpeg version 6.1...
============================================================

 * Running on http://127.0.0.1:5000
```

🎉 **conservatory.ai is now running!**

If you see `✗ FFmpeg NOT FOUND` here, go back to **Step 2** and install FFmpeg properly.

---

## Step 6: Open in Browser

Open Chrome, Firefox, Edge, or Safari and visit:

```
http://localhost:5000
```

You'll see the conservatory.ai interface. 🎼

---

# 🎙️ How to Use

## Recording Modes

Two ways to provide audio:

### 📁 Upload File Mode
- Use any existing audio file: WAV, MP3, OGG, FLAC, M4A, WebM
- Maximum 50 MB
- Drag and drop or click to select

### 🎤 Live Recording Mode
- Records directly from your microphone in your browser
- Click the mic icon, allow permission, hit record
- Click stop when done

## For Best Results

- ✅ Make recordings **at least 15 seconds** long
- ✅ Include **both low and high notes** if possible
- ✅ A **vocalise** (ah-ah-ah), **arpeggio**, or **glissando** is ideal
- ✅ Record in a **quiet environment**
- ✅ Stay **15-30 cm (6-12 inches)** from the microphone
- ❌ **Don't** record with backing music — vocals must be isolated
- ❌ **Don't** speak — sing!

## What You'll See

Click "Analyze". After 10-30 seconds, you'll get a detailed report with 11 sections:

1. Voice Type Classification
2. Range & Tessitura
3. Pitch Contour visualization
4. Passaggio (transition zones)
5. Vibrato Analysis
6. Vocal Health Indicators
7. Formant Analysis
8. Dynamic Range
9. Instructor Assessment (strengths, recommendations, warnings)
10. **Repertoire Guide** (classical and modern recommendations)

You can download a JSON report for your records.

---

# 🐛 Troubleshooting

## "Error: Analysis error: NoBackendError" or "Not an audio file"

**Cause**: FFmpeg is not installed or not in your PATH.

**Fix**: Go back to **Installation Step 2** and install FFmpeg. Then:
- Close ALL terminal windows
- Open a new terminal
- Verify with `ffmpeg -version`
- Restart `python app.py`
- Hard refresh browser (`Ctrl+F5` or `Cmd+Shift+R`)

The startup banner should show `✓ FFmpeg detected`.

## "Error: Chart is not defined"

**Cause**: A browser extension is blocking Chart.js.

**Fix**: This version loads Chart.js locally to avoid this. Make sure you're using the latest version (with `chart.min.js` in `static/js/`). Hard refresh the browser.

## "ModuleNotFoundError: No module named 'flask'"

**Cause**: You forgot to install dependencies, or your virtual environment isn't active.

**Fix**:
```bash
# Activate venv first
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Then install
pip install -r requirements.txt
```

## "Address already in use" (Port 5000 busy)

**Cause**: Another app is using port 5000 (often AirPlay on macOS, or another dev server).

**Fix**: Either close that app, or change conservatory.ai's port. In `app.py`, change the last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access via `http://localhost:5001`.

## Microphone permission denied

**Fix**: Click the lock icon in the address bar → **Site settings** → **Microphone** → **Allow**.

## Live recording works but file upload doesn't (or vice versa)

**Fix**: Make sure your file is one of these formats: WAV, MP3, OGG, FLAC, M4A, WebM. Other formats won't work.

## Analysis takes forever or hangs

- Recording might be too long (try 15-30 seconds)
- Your computer might be low on RAM (close other apps)
- The audio file might be corrupted (try another recording)
- Make sure FFmpeg is installed (long files require conversion)

## Live recording shows error but file upload works

**This is the FFmpeg problem.** Browser recordings come in WebM format, which requires FFmpeg to convert. Install FFmpeg from **Step 2**.

---

# 📁 Project Structure

```
voice_analyzer/
│
├── app.py                       # Flask server with FFmpeg auto-conversion
├── voice_analyzer.py            # Analysis engine — the heart of the project
├── repertoire_guide.py          # Repertoire database for 11 voice types
├── requirements.txt             # Python dependencies
│
├── templates/
│   └── index.html              # Single-page application
│
├── static/
│   ├── css/
│   │   └── style.css           # Editorial dark theme
│   └── js/
│       ├── app.js              # Frontend logic
│       ├── translations.js     # 15 language translations
│       └── chart.min.js        # Chart.js (local, no CDN dependency)
│
├── uploads/                     # Temporary audio files (auto-cleaned)
└── reports/                     # Saved JSON reports
```

---

# 🔬 Technical Details

## Algorithms

| Task | Method | Library |
|------|--------|---------|
| Pitch detection | PYIN (Probabilistic YIN) | librosa |
| Jitter/Shimmer | Praat algorithms | parselmouth |
| Formant analysis | Burg LPC method | parselmouth |
| Vibrato detection | FFT spectral analysis | numpy/scipy |
| Voice classification | Tessitura (60%) + Range (40%) weighted scoring | custom |
| Audio conversion | WebM/MP3/M4A → WAV (22050 Hz mono) | FFmpeg |

## Reference Values

```
Healthy vocal indicators (Praat standards):
├─ Jitter (Local) < 1.04%
├─ Shimmer (Local) < 3.81%
├─ HNR > 20 dB → very clean
├─ HNR 15-20 dB → normal
└─ HNR < 7 dB → significant breathiness

Ideal classical vibrato:
├─ Rate: 5-7 Hz
├─ Extent: 0.5-1 semitone
└─ Regular, controlled
```

## Supported Voice Types

**Female voices** (5):
1. Coloratura Soprano
2. Lyric Soprano
3. Dramatic Soprano
4. Mezzo-Soprano
5. Contralto

**Male voices** (6):
6. Countertenor
7. Lyric Tenor
8. Dramatic Tenor
9. Baritone
10. Bass-Baritone
11. Bass

---

# ⚠️ Important Disclaimer

> **This application performs acoustic analysis — it does NOT provide a definitive voice type diagnosis.**

For professional Fach determination:
- Live vocal assessment with a qualified teacher is required
- Voice timbre, weight, and ergonomics must also be evaluated
- Tessitura may not be fully captured from a single recording

**Health warning**: If your jitter or shimmer values are elevated, consider consulting an ENT specialist or laryngologist.

This system is a **guide and educational tool** — not a replacement for your vocal coach or doctor.

---

# 🛠️ Developer Notes

## Adding a New Language

1. Open `static/js/translations.js`
2. Copy an existing language block (e.g., `en: { ... }`)
3. Add the new language code (e.g., `it: { name: 'Italiano', flag: '🇮🇹', ... }`)
4. Translate all keys
5. If RTL, add to `RTL_LANGUAGES` array

## Adding a New Voice Type or Repertoire

Update the `REPERTOIRE_GUIDE` dictionary in `repertoire_guide.py`. Then update the `VOICE_TYPES` dictionary in `voice_analyzer.py` with corresponding frequency ranges.

## Adding a New Analysis Parameter

1. Add an `analyze_X()` method to `VoiceAnalyzer` class in `voice_analyzer.py`
2. Call it from `full_analysis()`
3. Add display logic to HTML and `app.js`

---

# 🎵 Philosophy

> *"La voce è l'anima fatta suono."*  
> *(The voice is the soul made sound.)*

This project combines modern scientific voice analysis with centuries-old vocal pedagogy traditions. The goal is to give voice artists a mirror to know their own voices more deeply — not to replace human teachers.

---

# 📝 License

MIT — use, modify, share freely.

# 🙏 Acknowledgments

- **The Praat team** (Boersma & Weenink) — industry-standard acoustic analysis
- **librosa developers** — modern music information retrieval library
- **parselmouth team** — bridge bringing Praat into Python
- **FFmpeg developers** — making audio processing universal
- All vocal coaches and pedagogues — for their accumulated wisdom

---

<div align="center">

**conservatory.ai**

*Made with ♪ for singers everywhere*

</div>
