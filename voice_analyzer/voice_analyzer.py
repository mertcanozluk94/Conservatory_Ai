"""
Profesyonel Ses Analiz Motoru
Konservatuar standartlarında vokal analizi
"""

import numpy as np
import librosa
import parselmouth
from parselmouth.praat import call
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')


# Nota frekansları sözlüğü (A4 = 440 Hz referans)
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Ses türü referans aralıkları (Hz cinsinden tipik aralıklar)
VOICE_TYPES = {
    # Kadın sesleri
    'Coloratura Soprano': {'low': 261.63, 'high': 1396.91, 'tessitura': (440, 880), 'gender': 'F'},  # C4 - F6
    'Lirik Soprano':      {'low': 246.94, 'high': 1046.50, 'tessitura': (392, 784), 'gender': 'F'},  # B3 - C6
    'Dramatik Soprano':   {'low': 220.00, 'high': 987.77,  'tessitura': (349, 698), 'gender': 'F'},  # A3 - B5
    'Mezzo-Soprano':      {'low': 196.00, 'high': 880.00,  'tessitura': (294, 587), 'gender': 'F'},  # G3 - A5
    'Kontralto':          {'low': 174.61, 'high': 698.46,  'tessitura': (220, 523), 'gender': 'F'},  # F3 - F5
    # Erkek sesleri
    'Kontratenor':        {'low': 196.00, 'high': 880.00,  'tessitura': (294, 587), 'gender': 'M'},  # G3 - A5
    'Lirik Tenor':        {'low': 130.81, 'high': 523.25,  'tessitura': (196, 392), 'gender': 'M'},  # C3 - C5
    'Dramatik Tenor':     {'low': 123.47, 'high': 493.88,  'tessitura': (174, 349), 'gender': 'M'},  # B2 - B4
    'Bariton':            {'low': 98.00,  'high': 392.00,  'tessitura': (146, 293), 'gender': 'M'},  # G2 - G4
    'Bas-Bariton':        {'low': 87.31,  'high': 349.23,  'tessitura': (130, 261), 'gender': 'M'},  # F2 - F4
    'Bas':                {'low': 82.41,  'high': 329.63,  'tessitura': (110, 220), 'gender': 'M'},  # E2 - E4
}


def hz_to_note(frequency):
    """Frekansı nota ismine çevirir (örn. 440 Hz -> A4)"""
    if frequency <= 0 or np.isnan(frequency):
        return None
    
    # A4 = 440 Hz referans alınarak yarım ton sayısı
    semitones_from_a4 = 12 * np.log2(frequency / 440.0)
    note_number = int(round(semitones_from_a4)) + 57  # A4 = MIDI 69, ama biz C0'ı 0 alıyoruz
    
    if note_number < 0:
        return None
    
    octave = note_number // 12
    note_index = note_number % 12
    return f"{NOTE_NAMES[note_index]}{octave}"


def note_to_hz(note_str):
    """Nota ismini frekansa çevirir (örn. A4 -> 440 Hz)"""
    if not note_str or len(note_str) < 2:
        return None
    try:
        if '#' in note_str:
            note = note_str[:2]
            octave = int(note_str[2:])
        else:
            note = note_str[0]
            octave = int(note_str[1:])
        
        note_index = NOTE_NAMES.index(note)
        note_number = octave * 12 + note_index
        semitones_from_a4 = note_number - 57
        return 440.0 * (2 ** (semitones_from_a4 / 12))
    except (ValueError, IndexError):
        return None


class VoiceAnalyzer:
    """Profesyonel ses analizi sınıfı"""
    
    def __init__(self, audio_path):
        self.audio_path = audio_path
        # librosa ile yükle (analiz için)
        self.y, self.sr = librosa.load(audio_path, sr=22050, mono=True)
        # Praat sound objesi (formant ve jitter için)
        self.sound = parselmouth.Sound(audio_path)
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)
        
        # Pitch verilerini önbelleğe al
        self._pitch_values = None
        self._pitch_times = None
    
    def extract_pitch(self, fmin=65, fmax=1500):
        """
        F0 (temel frekans) çıkarımı - PYIN algoritması
        İnsan sesi aralığı: 65 Hz (C2) - 1500 Hz (yaklaşık F#6)
        """
        if self._pitch_values is not None:
            return self._pitch_values, self._pitch_times
        
        f0, voiced_flag, voiced_probs = librosa.pyin(
            self.y,
            fmin=fmin,
            fmax=fmax,
            sr=self.sr,
            frame_length=2048
        )
        
        times = librosa.times_like(f0, sr=self.sr)
        
        # Sadece geçerli (sesli) frame'leri al
        valid_mask = ~np.isnan(f0) & voiced_flag
        self._pitch_values = f0[valid_mask]
        self._pitch_times = times[valid_mask]
        
        return self._pitch_values, self._pitch_times
    
    def analyze_range(self):
        """Ses aralığı analizi - min, max, medyan, ortalama"""
        pitches, _ = self.extract_pitch()
        
        if len(pitches) == 0:
            return None
        
        # Aşırı değerleri filtrele (en üst ve en alt %2'lik dilim - olası hata)
        p2 = np.percentile(pitches, 2)
        p98 = np.percentile(pitches, 98)
        filtered = pitches[(pitches >= p2) & (pitches <= p98)]
        
        min_freq = float(np.min(filtered))
        max_freq = float(np.max(filtered))
        median_freq = float(np.median(filtered))
        mean_freq = float(np.mean(filtered))
        
        # Oktav sayısı hesabı
        octaves = np.log2(max_freq / min_freq)
        
        return {
            'min_hz': round(min_freq, 2),
            'max_hz': round(max_freq, 2),
            'median_hz': round(median_freq, 2),
            'mean_hz': round(mean_freq, 2),
            'min_note': hz_to_note(min_freq),
            'max_note': hz_to_note(max_freq),
            'median_note': hz_to_note(median_freq),
            'octave_range': round(octaves, 2),
            'semitone_range': round(octaves * 12, 1)
        }
    
    def analyze_tessitura(self):
        """
        Tessitura analizi - sesin en sık kullandığı, en rahat çalıştığı bölge
        Histogram zirvelerine bakarak bulunur
        """
        pitches, _ = self.extract_pitch()
        
        if len(pitches) == 0:
            return None
        
        # Yarım ton (semitone) bazında histogram
        log_pitches = 12 * np.log2(pitches / 440.0)  # A4 = 0
        
        hist, bin_edges = np.histogram(log_pitches, bins=50)
        
        # Yoğunluğun %25-%75 arası tessitura olarak kabul edilir
        sorted_pitches = np.sort(pitches)
        q25 = float(np.percentile(sorted_pitches, 25))
        q75 = float(np.percentile(sorted_pitches, 75))
        
        # En yoğun frekansı bul (mode)
        peak_bin = np.argmax(hist)
        comfortable_log = (bin_edges[peak_bin] + bin_edges[peak_bin + 1]) / 2
        comfortable_freq = 440.0 * (2 ** (comfortable_log / 12))
        
        return {
            'low_hz': round(q25, 2),
            'high_hz': round(q75, 2),
            'low_note': hz_to_note(q25),
            'high_note': hz_to_note(q75),
            'comfortable_hz': round(float(comfortable_freq), 2),
            'comfortable_note': hz_to_note(comfortable_freq)
        }
    
    def analyze_vibrato(self):
        """
        Vibrato analizi
        - Hız (rate): Tipik değer 5-7 Hz
        - Genlik (extent): Yarım ton cinsinden
        """
        pitches, times = self.extract_pitch()
        
        if len(pitches) < 100:
            return None
        
        # Pitch'i yarım tona çevir (logaritmik ölçek)
        log_pitches = 12 * np.log2(pitches / np.median(pitches))
        
        # Trend'i çıkar (detrend)
        from scipy.signal import detrend
        detrended = detrend(log_pitches)
        
        # FFT ile dominant frekansı bul
        dt = np.median(np.diff(times)) if len(times) > 1 else 0.01
        if dt <= 0:
            return None
            
        fs = 1.0 / dt  # sampling rate of pitch contour
        n = len(detrended)
        
        if n < 4:
            return None
        
        fft_vals = np.abs(np.fft.rfft(detrended))
        fft_freqs = np.fft.rfftfreq(n, d=dt)
        
        # Vibrato 4-8 Hz aralığında aranır
        vibrato_band = (fft_freqs >= 4) & (fft_freqs <= 8)
        
        if not np.any(vibrato_band):
            return {'rate_hz': 0, 'extent_semitones': 0, 'has_vibrato': False, 'quality': 'Tespit edilemedi'}
        
        band_vals = fft_vals[vibrato_band]
        band_freqs = fft_freqs[vibrato_band]
        
        peak_idx = np.argmax(band_vals)
        vibrato_rate = float(band_freqs[peak_idx])
        
        # Genlik (peak-to-peak / 2, yarım ton cinsinden)
        vibrato_extent = float(np.std(detrended) * np.sqrt(2))
        
        # Vibrato kalitesi değerlendirmesi
        has_vibrato = vibrato_extent > 0.3 and 4.5 <= vibrato_rate <= 7.5
        
        if has_vibrato:
            if 5.5 <= vibrato_rate <= 6.5 and 0.5 <= vibrato_extent <= 1.0:
                quality = 'İdeal (Klasik standart)'
            elif vibrato_rate < 5:
                quality = 'Yavaş vibrato (wobble riski)'
            elif vibrato_rate > 7:
                quality = 'Hızlı vibrato (tremolo riski)'
            else:
                quality = 'Kabul edilebilir'
        else:
            quality = 'Belirgin vibrato yok (düz ses)'
        
        return {
            'rate_hz': round(vibrato_rate, 2),
            'extent_semitones': round(vibrato_extent, 2),
            'has_vibrato': has_vibrato,
            'quality': quality
        }
    
    def analyze_jitter_shimmer(self):
        """
        Jitter (perde kararsızlığı) ve Shimmer (genlik kararsızlığı)
        Ses sağlığı göstergeleri - Praat ile hesaplanır
        Normal değerler: Jitter < %1.04, Shimmer < %3.81
        """
        try:
            point_process = call(self.sound, "To PointProcess (periodic, cc)", 75, 600)
            
            jitter_local = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
            jitter_rap = call(point_process, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
            
            shimmer_local = call([self.sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            shimmer_apq3 = call([self.sound, point_process], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            
            # NaN kontrolü
            if np.isnan(jitter_local):
                jitter_local = 0
            if np.isnan(shimmer_local):
                shimmer_local = 0
            
            # Sağlık değerlendirmesi
            jitter_pct = jitter_local * 100
            shimmer_pct = shimmer_local * 100
            
            if jitter_pct < 1.04 and shimmer_pct < 3.81:
                health_status = 'Sağlıklı ses (Normal aralık)'
            elif jitter_pct < 2.0 and shimmer_pct < 6.0:
                health_status = 'Hafif düzensizlik'
            else:
                health_status = 'Belirgin düzensizlik (vokal sağlık kontrolü önerilir)'
            
            return {
                'jitter_local_pct': round(jitter_pct, 3),
                'jitter_rap_pct': round(jitter_rap * 100, 3) if not np.isnan(jitter_rap) else 0,
                'shimmer_local_pct': round(shimmer_pct, 3),
                'shimmer_apq3_pct': round(shimmer_apq3 * 100, 3) if not np.isnan(shimmer_apq3) else 0,
                'health_status': health_status
            }
        except Exception as e:
            return {
                'jitter_local_pct': 0,
                'jitter_rap_pct': 0,
                'shimmer_local_pct': 0,
                'shimmer_apq3_pct': 0,
                'health_status': 'Hesaplanamadı (yetersiz periyodik sinyal)'
            }
    
    def analyze_hnr(self):
        """
        Harmonics-to-Noise Ratio - ses temizliği göstergesi
        > 20 dB: Çok temiz, > 15 dB: Normal, < 7 dB: Belirgin nefes/kısıklık
        """
        try:
            harmonicity = call(self.sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
            hnr = call(harmonicity, "Get mean", 0, 0)
            
            if np.isnan(hnr):
                hnr = 0
            
            if hnr > 20:
                quality = 'Çok temiz, parlak ses'
            elif hnr > 15:
                quality = 'Normal, sağlıklı ses'
            elif hnr > 10:
                quality = 'Hafif nefesli/havalı ses'
            elif hnr > 7:
                quality = 'Belirgin nefes/havalılık'
            else:
                quality = 'Kısık veya çok nefesli ses'
            
            return {
                'hnr_db': round(hnr, 2),
                'quality': quality
            }
        except Exception:
            return {'hnr_db': 0, 'quality': 'Hesaplanamadı'}
    
    def analyze_formants(self):
        """
        Formant analizi (F1, F2, F3) ve Singer's Formant
        Singer's Formant (2800-3200 Hz): Operatik seslerin parlaklık kaynağı
        """
        try:
            formant = call(self.sound, "To Formant (burg)", 0.01, 5, 5500, 0.025, 50)
            
            # Sesli kısımların ortasında formant ölç
            duration = self.sound.duration
            sample_times = np.linspace(duration * 0.2, duration * 0.8, 20)
            
            f1_vals, f2_vals, f3_vals = [], [], []
            
            for t in sample_times:
                f1 = call(formant, "Get value at time", 1, t, 'Hertz', 'Linear')
                f2 = call(formant, "Get value at time", 2, t, 'Hertz', 'Linear')
                f3 = call(formant, "Get value at time", 3, t, 'Hertz', 'Linear')
                
                if not np.isnan(f1):
                    f1_vals.append(f1)
                if not np.isnan(f2):
                    f2_vals.append(f2)
                if not np.isnan(f3):
                    f3_vals.append(f3)
            
            f1_mean = float(np.mean(f1_vals)) if f1_vals else 0
            f2_mean = float(np.mean(f2_vals)) if f2_vals else 0
            f3_mean = float(np.mean(f3_vals)) if f3_vals else 0
            
            # Singer's Formant kontrolü (2800-3200 Hz arasında belirgin enerji)
            # Spektral analiz ile
            stft = np.abs(librosa.stft(self.y))
            freqs = librosa.fft_frequencies(sr=self.sr)
            
            singers_formant_band = (freqs >= 2800) & (freqs <= 3200)
            other_band = (freqs >= 1000) & (freqs <= 2800)
            
            sf_energy = np.mean(stft[singers_formant_band, :])
            other_energy = np.mean(stft[other_band, :])
            
            sf_ratio = sf_energy / (other_energy + 1e-10)
            has_singers_formant = sf_ratio > 0.3
            
            return {
                'f1_hz': round(f1_mean, 1),
                'f2_hz': round(f2_mean, 1),
                'f3_hz': round(f3_mean, 1),
                'singers_formant_ratio': round(float(sf_ratio), 3),
                'has_singers_formant': has_singers_formant,
                'singers_formant_status': 'Mevcut (Operatik parlaklık)' if has_singers_formant else 'Belirgin değil'
            }
        except Exception:
            return {
                'f1_hz': 0, 'f2_hz': 0, 'f3_hz': 0,
                'singers_formant_ratio': 0,
                'has_singers_formant': False,
                'singers_formant_status': 'Hesaplanamadı'
            }
    
    def detect_passaggio(self):
        """
        Passaggio (geçiş bölgesi) tahmini
        Cinsiyet ve sese göre tipik passaggio noktaları:
        - Soprano: E4-F#4 (primo), F5-G5 (secondo)
        - Mezzo: D4-E4 (primo), E5-F5 (secondo)
        - Tenor: D4-E4 (primo), F#4-G4 (secondo)
        - Bariton: B3-C4 (primo), E4-F4 (secondo)
        - Bas: A3-B3 (primo), D4-E4 (secondo)
        """
        range_data = self.analyze_range()
        if not range_data:
            return None
        
        median_hz = range_data['median_hz']
        
        # Medyan frekansa göre tahmin
        if median_hz > 350:  # Soprano bölgesi
            primo = ('E4', 329.63)
            secondo = ('F5', 698.46)
        elif median_hz > 280:  # Mezzo
            primo = ('D4', 293.66)
            secondo = ('E5', 659.25)
        elif median_hz > 200:  # Tenor
            primo = ('D4', 293.66)
            secondo = ('F#4', 369.99)
        elif median_hz > 150:  # Bariton
            primo = ('B3', 246.94)
            secondo = ('E4', 329.63)
        else:  # Bas
            primo = ('A3', 220.00)
            secondo = ('D4', 293.66)
        
        return {
            'primo_passaggio_note': primo[0],
            'primo_passaggio_hz': primo[1],
            'secondo_passaggio_note': secondo[0],
            'secondo_passaggio_hz': secondo[1],
            'note': 'Bu değerler medyan frekansa göre yaklaşık tahmindir. Kesin tespit için canlı vokal değerlendirme gereklidir.'
        }
    
    def classify_voice_type(self):
        """
        Ses türü sınıflandırması - Fach sistemi
        Range, tessitura ve formant bilgilerini kullanır
        """
        range_data = self.analyze_range()
        tessitura_data = self.analyze_tessitura()
        
        if not range_data or not tessitura_data:
            return None
        
        min_freq = range_data['min_hz']
        max_freq = range_data['max_hz']
        tess_low = tessitura_data['low_hz']
        tess_high = tessitura_data['high_hz']
        
        # Her ses türü için uygunluk skoru hesapla
        scores = {}
        for voice_type, ref in VOICE_TYPES.items():
            # Range uyumu (0-1)
            range_match = 0
            if min_freq <= ref['low'] * 1.15 and max_freq >= ref['high'] * 0.85:
                range_match = 1.0
            elif min_freq <= ref['low'] * 1.3 and max_freq >= ref['high'] * 0.7:
                range_match = 0.6
            else:
                # Kısmi örtüşme
                overlap_low = max(min_freq, ref['low'])
                overlap_high = min(max_freq, ref['high'])
                if overlap_high > overlap_low:
                    overlap = (overlap_high - overlap_low) / (ref['high'] - ref['low'])
                    range_match = max(0, overlap * 0.5)
            
            # Tessitura uyumu (daha önemli!)
            ref_tess_low, ref_tess_high = ref['tessitura']
            tess_overlap_low = max(tess_low, ref_tess_low)
            tess_overlap_high = min(tess_high, ref_tess_high)
            
            tess_match = 0
            if tess_overlap_high > tess_overlap_low:
                tess_match = (tess_overlap_high - tess_overlap_low) / (ref_tess_high - ref_tess_low)
            
            # Toplam skor (tessitura %60, range %40)
            scores[voice_type] = tess_match * 0.6 + range_match * 0.4
        
        # En yüksek 3 skoru al
        sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_3 = sorted_types[:3]
        
        primary = top_3[0]
        confidence = primary[1] * 100
        
        if confidence > 70:
            confidence_label = 'Yüksek güvenilirlik'
        elif confidence > 50:
            confidence_label = 'Orta güvenilirlik'
        else:
            confidence_label = 'Düşük güvenilirlik (daha uzun kayıt önerilir)'
        
        return {
            'primary_type': primary[0],
            'confidence_pct': round(confidence, 1),
            'confidence_label': confidence_label,
            'alternatives': [
                {'type': t[0], 'score': round(t[1] * 100, 1)} 
                for t in top_3[1:]
            ],
            'gender_estimate': VOICE_TYPES[primary[0]]['gender']
        }
    
    def analyze_dynamic_range(self):
        """Dinamik aralık analizi - desibel cinsinden"""
        # RMS enerji üzerinden
        rms = librosa.feature.rms(y=self.y, frame_length=2048, hop_length=512)[0]
        
        # Sessiz kısımları filtrele
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        active_db = rms_db[rms_db > -40]  # -40 dB altı sessizlik
        
        if len(active_db) == 0:
            return {'min_db': 0, 'max_db': 0, 'range_db': 0, 'description': 'Hesaplanamadı'}
        
        min_db = float(np.percentile(active_db, 5))
        max_db = float(np.percentile(active_db, 95))
        range_db = max_db - min_db
        
        if range_db > 30:
            desc = 'Çok geniş dinamik aralık (operatik)'
        elif range_db > 20:
            desc = 'Geniş dinamik aralık'
        elif range_db > 12:
            desc = 'Normal dinamik aralık'
        else:
            desc = 'Dar dinamik aralık'
        
        return {
            'min_db': round(min_db, 1),
            'max_db': round(max_db, 1),
            'range_db': round(range_db, 1),
            'description': desc
        }
    
    def get_pitch_contour_data(self):
        """Pitch contour grafiği için veri"""
        pitches, times = self.extract_pitch()
        
        if len(pitches) == 0:
            return {'times': [], 'pitches': [], 'notes': []}
        
        # Performans için örnekle (max 500 nokta)
        if len(pitches) > 500:
            indices = np.linspace(0, len(pitches) - 1, 500).astype(int)
            pitches = pitches[indices]
            times = times[indices]
        
        return {
            'times': [round(float(t), 3) for t in times],
            'pitches': [round(float(p), 2) for p in pitches],
            'notes': [hz_to_note(p) for p in pitches]
        }
    
    def full_analysis(self):
        """Tam analiz - tüm parametreleri döndürür"""
        return {
            'duration_seconds': round(self.duration, 2),
            'sample_rate': self.sr,
            'range': self.analyze_range(),
            'tessitura': self.analyze_tessitura(),
            'voice_type': self.classify_voice_type(),
            'passaggio': self.detect_passaggio(),
            'vibrato': self.analyze_vibrato(),
            'jitter_shimmer': self.analyze_jitter_shimmer(),
            'hnr': self.analyze_hnr(),
            'formants': self.analyze_formants(),
            'dynamic_range': self.analyze_dynamic_range(),
            'pitch_contour': self.get_pitch_contour_data()
        }


def generate_recommendations(analysis):
    """
    Konservatuar eğitmeni perspektifinden öneriler üretir
    """
    recommendations = []
    warnings = []
    strengths = []
    
    # Range değerlendirmesi
    if analysis['range']:
        octaves = analysis['range']['octave_range']
        if octaves >= 2.5:
            strengths.append(f"Geniş ses aralığı ({octaves} oktav) — profesyonel düzeyde.")
        elif octaves >= 2.0:
            strengths.append(f"İyi ses aralığı ({octaves} oktav) — solo repertuar için yeterli.")
        elif octaves >= 1.5:
            recommendations.append(f"Ses aralığını ({octaves} oktav) genişletmek için hem alt hem üst registerlere yönelik teknik çalışmalar yapılmalı.")
        else:
            recommendations.append(f"Ses aralığı ({octaves} oktav) sınırlı. Düzenli vokalizasyon ve nefes egzersizleri ile geliştirilebilir.")
    
    # Vibrato değerlendirmesi
    if analysis['vibrato']:
        vib = analysis['vibrato']
        if 'İdeal' in vib['quality']:
            strengths.append(f"İdeal vibrato ({vib['rate_hz']} Hz) — klasik repertuar için mükemmel.")
        elif 'wobble' in vib['quality']:
            warnings.append(f"Vibrato hızı yavaş ({vib['rate_hz']} Hz). Kontrolsüz vibrato (wobble) riski var. Destekli nefes çalışmaları önerilir.")
        elif 'tremolo' in vib['quality']:
            warnings.append(f"Vibrato hızı yüksek ({vib['rate_hz']} Hz). Tremolo eğilimi var. Larenks pozisyonu ve gevşeme egzersizleri faydalı olur.")
        elif not vib['has_vibrato']:
            recommendations.append("Belirgin vibrato tespit edilmedi. Doğal vibrato gelişimi için 'messa di voce' ve sürekli ton egzersizleri faydalıdır.")
    
    # Jitter-Shimmer (vokal sağlık)
    if analysis['jitter_shimmer']:
        js = analysis['jitter_shimmer']
        if 'Sağlıklı' in js['health_status']:
            strengths.append("Vokal kıvrım (vocal fold) işlevi sağlıklı — düzenli, periyodik titreşim.")
        elif 'Belirgin' in js['health_status']:
            warnings.append(f"Jitter (%{js['jitter_local_pct']}) ve Shimmer (%{js['shimmer_local_pct']}) değerleri normalin üzerinde. Vokal yorgunluk veya hafif disfoni belirtisi olabilir. Bir KBB uzmanı/foniyatristen değerlendirme alınması önerilir.")
    
    # HNR (ses temizliği)
    if analysis['hnr']:
        hnr_val = analysis['hnr']['hnr_db']
        if hnr_val > 20:
            strengths.append(f"Yüksek harmonik/gürültü oranı ({hnr_val} dB) — parlak, temiz tını.")
        elif hnr_val < 10 and hnr_val > 0:
            recommendations.append(f"HNR değeri ({hnr_val} dB) düşük. Nefes desteği ve kıvrım kapanma çalışmaları (örn. straw phonation) önerilir.")
    
    # Singer's Formant
    if analysis['formants'] and analysis['formants']['has_singers_formant']:
        strengths.append("Singer's Formant mevcut (2800-3200 Hz bandı) — orkestrayı 'kesebilen' operatik tını kalitesi.")
    elif analysis['formants']:
        recommendations.append("Singer's Formant zayıf. Klasik repertuar için 'chiaroscuro' (parlaklık-koyuluk dengesi) çalışmaları faydalı olabilir.")
    
    # Ses türü güveni
    if analysis['voice_type']:
        vt = analysis['voice_type']
        if vt['confidence_pct'] < 50:
            recommendations.append("Ses türü tespiti düşük güvenilirlikte. Daha uzun süreli ve farklı registerleri içeren bir kayıt (en az 30 saniye, hem alt hem üst notalar) daha doğru sonuç verir.")
    
    return {
        'strengths': strengths,
        'recommendations': recommendations,
        'warnings': warnings
    }


def _json_safe(obj):
    """Recursively convert numpy types to native Python types for JSON"""
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_json_safe(x) for x in obj]
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        analyzer = VoiceAnalyzer(sys.argv[1])
        result = analyzer.full_analysis()
        recs = generate_recommendations(result)
        result['recommendations'] = recs
        
        import json
        print(json.dumps(_json_safe(result), indent=2, ensure_ascii=False))
