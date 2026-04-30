"""
conservatory.ai - Flask Backend
Ses analiz web uygulaması
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
import json
import subprocess
from datetime import datetime
from voice_analyzer import VoiceAnalyzer, generate_recommendations, _json_safe
from repertoire_guide import get_genre_recommendations

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'webm'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_wav(input_path, output_path):
    """
    FFmpeg kullanarak herhangi bir ses formatını WAV'a çevirir.
    Praat sadece WAV okuyabildiği için bu adım kritik.
    
    Returns:
        True: Dönüşüm başarılı
        False: FFmpeg hatası
    """
    try:
        # FFmpeg komutu:
        # -i: input file
        # -ar 22050: sample rate 22050 Hz (analiz için yeterli)
        # -ac 1: mono kanal
        # -y: çıktıyı sormadan üzerine yaz
        # -loglevel error: sadece hataları göster
        result = subprocess.run([
            'ffmpeg',
            '-i', input_path,
            '-ar', '22050',
            '-ac', '1',
            '-y',
            '-loglevel', 'error',
            output_path
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"FFmpeg hatası: {result.stderr}")
            return False
        
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0
        
    except FileNotFoundError:
        print("HATA: FFmpeg sistemde bulunamadı! Lütfen FFmpeg yükleyin.")
        return False
    except subprocess.TimeoutExpired:
        print("HATA: FFmpeg dönüşümü çok uzun sürdü (60s timeout)")
        return False
    except Exception as e:
        print(f"FFmpeg dönüşüm hatası: {e}")
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Ses dosyasını alıp analiz eder"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400
    
    file = request.files['audio']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file format. Accepted: wav, mp3, ogg, flac, m4a, webm'}), 400
    
    # Benzersiz dosya adı
    file_id = str(uuid.uuid4())
    extension = file.filename.rsplit('.', 1)[1].lower()
    original_filename = f"{file_id}.{extension}"
    original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    
    # Analiz için kullanılacak WAV dosyası
    wav_filename = f"{file_id}_analysis.wav"
    wav_filepath = os.path.join(app.config['UPLOAD_FOLDER'], wav_filename)
    
    files_to_cleanup = [original_filepath, wav_filepath]
    
    try:
        # Yüklenen dosyayı kaydet
        file.save(original_filepath)
        
        # WAV'a dönüştür (Praat sadece WAV okur, bu adım kritik!)
        # WAV bile olsa standart formata çevirelim (22050 Hz, mono)
        print(f"Dönüştürülüyor: {extension} -> wav")
        conversion_ok = convert_to_wav(original_filepath, wav_filepath)
        
        if not conversion_ok:
            # FFmpeg yoksa veya dönüşüm başarısız olduysa,
            # eğer dosya zaten WAV ise direkt onu kullan
            if extension == 'wav':
                wav_filepath = original_filepath
                files_to_cleanup = [original_filepath]
                print("FFmpeg yok, WAV dosyası direkt kullanılıyor")
            else:
                return jsonify({
                    'error': 'Audio conversion failed. Please install FFmpeg. '
                             'See: https://www.gyan.dev/ffmpeg/builds/ or run: winget install Gyan.FFmpeg'
                }), 500
        
        # Analiz yap
        print(f"Analiz başlıyor: {wav_filepath}")
        analyzer = VoiceAnalyzer(wav_filepath)
        result = analyzer.full_analysis()
        
        # Önerileri ekle
        recommendations = generate_recommendations(result)
        result['recommendations'] = recommendations
        result['analysis_id'] = file_id
        result['timestamp'] = datetime.now().isoformat()
        
        # Repertuvar rehberi ekle
        if result.get('voice_type') and result['voice_type'].get('primary_type'):
            primary_type = result['voice_type']['primary_type']
            repertoire = get_genre_recommendations(primary_type)
            if repertoire:
                result['repertoire'] = repertoire
        
        # Numpy tiplerini Python native'a çevir
        result = _json_safe(result)
        
        # Raporu kaydet
        report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{file_id}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return jsonify(result)
    
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print("=" * 60)
        print("ANALİZ HATASI:")
        print(error_detail)
        print("=" * 60)
        error_msg = str(e) if str(e) else type(e).__name__
        return jsonify({'error': f'Analysis error: {error_msg}'}), 500
    
    finally:
        # Geçici dosyaları temizle
        for filepath in files_to_cleanup:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Dosya silme hatası: {e}")


@app.route('/report/<analysis_id>')
def get_report(analysis_id):
    """Kaydedilmiş raporu getirir"""
    report_path = os.path.join(app.config['REPORTS_FOLDER'], f"{analysis_id}.json")
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True, download_name=f"voice_analysis_{analysis_id[:8]}.json")
    return jsonify({'error': 'Report not found'}), 404


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum 50 MB.'}), 413


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
    
    # FFmpeg kontrolü
    print("=" * 60)
    print("conservatory.ai - Voice Analysis Server")
    print("=" * 60)
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg detected: {version_line}")
        else:
            print("⚠ FFmpeg detected but returned error")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("✗ FFmpeg NOT FOUND in PATH!")
        print("  Live recording (webm) and most formats won't work.")
        print("  Install: winget install Gyan.FFmpeg  (Windows)")
        print("           brew install ffmpeg          (Mac)")
        print("           apt install ffmpeg           (Linux)")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
