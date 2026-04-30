/**
 * conservatory.ai — Frontend Logic
 */

// State
let currentMode = 'upload';
let selectedFile = null;
let mediaRecorder = null;
let audioChunks = [];
let recordingStartTime = null;
let recordingTimer = null;
let recordedBlob = null;
let pitchChart = null;
let lastAnalysisId = null;
let lastAnalysisData = null;

// DOM Elements
const fileInput = document.getElementById('file-input');
const uploadZone = document.getElementById('upload-zone');
const uploadArea = document.getElementById('upload-area');
const recordArea = document.getElementById('record-area');
const recordBtn = document.getElementById('record-btn');
const recordTime = document.getElementById('record-time');
const recordVisualizer = document.getElementById('record-visualizer');
const recordZone = document.querySelector('.record-zone');
const analyzeBtn = document.getElementById('analyze-btn');
const uploadSection = document.getElementById('upload-section');
const loadingSection = document.getElementById('loading-section');
const resultsSection = document.getElementById('results-section');
const loadingSubtext = document.getElementById('loading-substext');
const datestampEl = document.getElementById('datestamp');

// Date stamp
function updateDatestamp() {
    const now = new Date();
    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    datestampEl.textContent = `${now.getDate().toString().padStart(2, '0')} ${months[now.getMonth()]} ${now.getFullYear()}`;
}
updateDatestamp();

// =================== LANGUAGE SELECTOR ===================
function buildLanguageMenu() {
    const menu = document.getElementById('lang-menu');
    menu.innerHTML = '';
    Object.entries(TRANSLATIONS).forEach(([code, lang]) => {
        const item = document.createElement('button');
        item.className = 'lang-item';
        if (code === currentLang) item.classList.add('active');
        item.innerHTML = `<span class="lang-flag">${lang.flag}</span><span class="lang-name">${lang.name}</span>`;
        item.addEventListener('click', () => {
            setLanguage(code);
            updateLangSelector();
            buildLanguageMenu();
            menu.classList.remove('open');
            // Yeniden oluştur — repertuvar varsa
            if (lastAnalysisData) displayResults(lastAnalysisData, true);
        });
        menu.appendChild(item);
    });
}

function updateLangSelector() {
    const lang = TRANSLATIONS[currentLang];
    document.getElementById('current-lang-flag').textContent = lang.flag;
    document.getElementById('current-lang-name').textContent = lang.name;
}

document.getElementById('lang-toggle').addEventListener('click', (e) => {
    e.stopPropagation();
    document.getElementById('lang-menu').classList.toggle('open');
});

document.addEventListener('click', () => {
    document.getElementById('lang-menu').classList.remove('open');
});

// Initialize
setLanguage(currentLang);
updateLangSelector();
buildLanguageMenu();
applyTranslations();

// =================== MODE SWITCHING ===================
document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentMode = btn.dataset.mode;
        
        if (currentMode === 'upload') {
            uploadArea.style.display = 'block';
            recordArea.style.display = 'none';
        } else {
            uploadArea.style.display = 'none';
            recordArea.style.display = 'block';
        }
        
        selectedFile = null;
        recordedBlob = null;
        analyzeBtn.disabled = true;
    });
});

// =================== FILE UPLOAD ===================
uploadZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

function handleFile(file) {
    selectedFile = file;
    const sizeKB = (file.size / 1024).toFixed(0);
    document.querySelector('.upload-text').textContent = file.name;
    document.querySelector('.upload-hint').innerHTML = 
        `<strong>${sizeKB} KB</strong> · ${t('analyze')} ↓`;
    analyzeBtn.disabled = false;
}

// =================== RECORDING ===================
recordBtn.addEventListener('click', async () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        stopRecording();
    } else {
        await startRecording();
    }
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };
        
        mediaRecorder.onstop = () => {
            recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
            stream.getTracks().forEach(track => track.stop());
            analyzeBtn.disabled = false;
        };
        
        mediaRecorder.start();
        recordingStartTime = Date.now();
        recordZone.classList.add('recording');
        recordBtn.querySelector('.record-label').textContent = t('record_stop');
        
        recordingTimer = setInterval(() => {
            const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
            const min = Math.floor(elapsed / 60).toString().padStart(2, '0');
            const sec = (elapsed % 60).toString().padStart(2, '0');
            recordTime.textContent = `${min}:${sec}`;
        }, 100);
        
        animateVisualizer(stream);
        
    } catch (err) {
        alert(t('error_mic') + ': ' + err.message);
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        clearInterval(recordingTimer);
        recordZone.classList.remove('recording');
        recordBtn.querySelector('.record-label').textContent = t('record_again');
    }
}

function animateVisualizer(stream) {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaStreamSource(stream);
    source.connect(analyser);
    analyser.fftSize = 64;
    
    const bars = recordVisualizer.querySelectorAll('.vis-bar');
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    
    function draw() {
        if (!recordZone.classList.contains('recording')) return;
        analyser.getByteFrequencyData(dataArray);
        bars.forEach((bar, i) => {
            const value = dataArray[i * 2] || 0;
            const height = 8 + (value / 255) * 60;
            bar.style.height = `${height}px`;
        });
        requestAnimationFrame(draw);
    }
    draw();
}

// =================== ANALYZE ===================
analyzeBtn.addEventListener('click', async () => {
    const formData = new FormData();
    
    if (currentMode === 'upload' && selectedFile) {
        formData.append('audio', selectedFile);
    } else if (currentMode === 'record' && recordedBlob) {
        formData.append('audio', recordedBlob, 'recording.webm');
    } else {
        return;
    }
    
    formData.append('lang', currentLang);
    
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    const messages = TRANSLATIONS[currentLang].loading_messages;
    let msgIdx = 0;
    const msgInterval = setInterval(() => {
        loadingSubtext.textContent = messages[msgIdx % messages.length];
        msgIdx++;
    }, 1200);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(msgInterval);
        
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || 'Error');
        }
        
        const data = await response.json();
        lastAnalysisId = data.analysis_id;
        lastAnalysisData = data;
        displayResults(data);
        
    } catch (err) {
        clearInterval(msgInterval);
        loadingSection.style.display = 'none';
        uploadSection.style.display = 'block';
        alert('Error: ' + err.message);
    }
});

// =================== DISPLAY RESULTS ===================
function displayResults(data, langChange = false) {
    if (!langChange) {
        loadingSection.style.display = 'none';
        resultsSection.style.display = 'block';
    }
    
    if (data.voice_type) {
        document.getElementById('voice-type-name').textContent = data.voice_type.primary_type;
        document.getElementById('voice-type-confidence').textContent = `${t('confidence')}: %${data.voice_type.confidence_pct}`;
        document.getElementById('voice-type-label').textContent = mapConfidenceLabel(data.voice_type.confidence_label);
        
        // Düşük güven uyarısı (< %60)
        const lcWarning = document.getElementById('low-confidence-warning');
        if (lcWarning) {
            if (data.voice_type.confidence_pct < 60) {
                lcWarning.style.display = 'flex';
            } else {
                lcWarning.style.display = 'none';
            }
        }
        
        const altsHTML = data.voice_type.alternatives.map(a => 
            `<span class="alt-item">${a.type}<span class="alt-score">%${a.score}</span></span>`
        ).join('');
        document.getElementById('alternatives').innerHTML = altsHTML;
    }
    
    if (data.range) {
        document.getElementById('min-note').textContent = data.range.min_note || '—';
        document.getElementById('max-note').textContent = data.range.max_note || '—';
        document.getElementById('min-hz').textContent = `${data.range.min_hz} Hz`;
        document.getElementById('max-hz').textContent = `${data.range.max_hz} Hz`;
        document.getElementById('octave-range').textContent = data.range.octave_range;
        document.getElementById('semitone-range').textContent = data.range.semitone_range;
    }
    
    if (data.tessitura) {
        document.getElementById('tess-low').textContent = data.tessitura.low_note || '—';
        document.getElementById('tess-high').textContent = data.tessitura.high_note || '—';
        document.getElementById('comfortable-note').textContent = data.tessitura.comfortable_note || '—';
    }
    
    if (data.passaggio) {
        document.getElementById('primo-passaggio').textContent = data.passaggio.primo_passaggio_note;
        document.getElementById('secondo-passaggio').textContent = data.passaggio.secondo_passaggio_note;
    }
    
    if (data.vibrato) {
        document.getElementById('vibrato-rate').textContent = data.vibrato.rate_hz;
        document.getElementById('vibrato-extent').textContent = data.vibrato.extent_semitones;
        document.getElementById('vibrato-quality').textContent = data.vibrato.quality;
    }
    
    if (data.jitter_shimmer) {
        document.getElementById('jitter').textContent = data.jitter_shimmer.jitter_local_pct;
        document.getElementById('shimmer').textContent = data.jitter_shimmer.shimmer_local_pct;
        document.getElementById('health-status').textContent = data.jitter_shimmer.health_status;
    }
    if (data.hnr) {
        document.getElementById('hnr').textContent = data.hnr.hnr_db;
    }
    
    if (data.formants) {
        document.getElementById('f1').textContent = data.formants.f1_hz;
        document.getElementById('f2').textContent = data.formants.f2_hz;
        document.getElementById('f3').textContent = data.formants.f3_hz;
        document.getElementById('singers-formant').textContent = data.formants.singers_formant_status;
    }
    
    if (data.dynamic_range) {
        document.getElementById('dynamic-min').textContent = data.dynamic_range.min_db;
        document.getElementById('dynamic-max').textContent = data.dynamic_range.max_db;
        document.getElementById('dynamic-range').textContent = data.dynamic_range.range_db;
        document.getElementById('dynamic-desc').textContent = data.dynamic_range.description;
    }
    
    if (data.recommendations) {
        renderList('strengths-list', data.recommendations.strengths, t('empty_strengths'));
        renderList('recommendations-list', data.recommendations.recommendations, t('empty_suggestions'));
        renderList('warnings-list', data.recommendations.warnings, t('empty_warnings'));
    }
    
    // Repertoire Guide
    if (data.repertoire) {
        document.getElementById('rep-description').textContent = data.repertoire.description;
        renderList('classical-genres-list', data.repertoire.classical_genres);
        renderList('modern-genres-list', data.repertoire.modern_genres);
        renderList('classical-rep-list', data.repertoire.classical_repertoire);
        renderList('modern-rep-list', data.repertoire.modern_repertoire);
        document.getElementById('avoid-text').textContent = data.repertoire.avoid;
        document.getElementById('training-tips-text').textContent = data.repertoire.training_tips;
        document.getElementById('repertoire-section').style.display = 'block';
    } else {
        document.getElementById('repertoire-section').style.display = 'none';
    }
    
    if (data.pitch_contour && data.pitch_contour.times.length > 0) {
        renderPitchChart(data.pitch_contour);
    }
    
    if (!langChange) {
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }
}

function mapConfidenceLabel(originalLabel) {
    // Eski Türkçe etiketleri çevir
    if (originalLabel.includes('Yüksek') || originalLabel.includes('High')) return t('confidence_high');
    if (originalLabel.includes('Orta') || originalLabel.includes('Medium')) return t('confidence_med');
    if (originalLabel.includes('Düşük') || originalLabel.includes('Low')) return t('confidence_low');
    return originalLabel;
}

function renderList(elementId, items, emptyMsg = '') {
    const el = document.getElementById(elementId);
    if (!items || items.length === 0) {
        el.innerHTML = emptyMsg ? `<li class="empty">${emptyMsg}</li>` : '';
    } else {
        el.innerHTML = items.map(item => `<li>${item}</li>`).join('');
    }
}

function renderPitchChart(contour) {
    // Chart.js yüklenmemişse sessizce atla
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js yüklenemedi, pitch contour grafiği atlanıyor');
        const canvas = document.getElementById('pitchChart');
        if (canvas && canvas.parentElement) {
            canvas.parentElement.innerHTML = '<p style="text-align:center;color:#8a8270;font-family:var(--mono);font-size:11px;letter-spacing:0.2em;padding:60px 20px;">PITCH CONTOUR GRAFİĞİ YÜKLENEMEDİ<br><span style="font-size:10px;opacity:0.6;">Chart.js kütüphanesi tarayıcı tarafından bloklandı</span></p>';
        }
        return;
    }
    
    const ctx = document.getElementById('pitchChart').getContext('2d');
    if (pitchChart) pitchChart.destroy();
    
    pitchChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: contour.times,
            datasets: [{
                label: 'Pitch (Hz)',
                data: contour.pitches,
                borderColor: '#c4923a',
                backgroundColor: 'rgba(196, 146, 58, 0.1)',
                borderWidth: 1.5,
                pointRadius: 0,
                tension: 0.2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#161410',
                    titleColor: '#f4ede0',
                    bodyColor: '#c8bfa9',
                    borderColor: '#3d382e',
                    borderWidth: 1,
                    padding: 12,
                    titleFont: { family: "'JetBrains Mono', monospace", size: 11 },
                    bodyFont: { family: "'Cormorant Garamond', serif", size: 14 },
                    callbacks: {
                        title: (items) => `t = ${items[0].label}s`,
                        label: (item) => {
                            const idx = item.dataIndex;
                            const note = contour.notes[idx];
                            return `${item.parsed.y} Hz · ${note || ''}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Time (s)', color: '#8a8270', font: { family: "'JetBrains Mono', monospace", size: 10 } },
                    ticks: { color: '#8a8270', font: { family: "'JetBrains Mono', monospace", size: 10 }, maxTicksLimit: 8 },
                    grid: { color: 'rgba(61, 56, 46, 0.4)' }
                },
                y: {
                    title: { display: true, text: 'Frequency (Hz)', color: '#8a8270', font: { family: "'JetBrains Mono', monospace", size: 10 } },
                    ticks: { color: '#8a8270', font: { family: "'JetBrains Mono', monospace", size: 10 } },
                    grid: { color: 'rgba(61, 56, 46, 0.4)' }
                }
            }
        }
    });
}

// =================== ACTIONS ===================
document.getElementById('download-report').addEventListener('click', () => {
    if (lastAnalysisId) {
        window.location.href = `/report/${lastAnalysisId}`;
    }
});

document.getElementById('new-analysis').addEventListener('click', () => {
    resultsSection.style.display = 'none';
    uploadSection.style.display = 'block';
    selectedFile = null;
    recordedBlob = null;
    fileInput.value = '';
    document.querySelector('.upload-text').textContent = t('upload_text');
    document.querySelector('.upload-hint').textContent = t('upload_hint');
    analyzeBtn.disabled = true;
    recordTime.textContent = '00:00';
    if (recordBtn.querySelector('.record-label')) {
        recordBtn.querySelector('.record-label').textContent = t('record_start');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
