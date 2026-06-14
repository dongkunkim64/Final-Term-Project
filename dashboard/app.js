// --- Simulation & UI State ---
let activeAttack = 'none'; // 'none', 'steering_takeover', 'gps_spoofing', etc.
let fheEnabled = true;
let selectedModel = 'lr'; // 'lr' or 'dt'

// Latency constants from fhe_results.json
const LATENCY_DATA = {
    lr: { plain: 0.0117, fhe: 35.3254, name: 'Logistic Regression' },
    dt: { plain: 0.0121, fhe: 45.9935, name: 'Decision Tree' }
};

// Cumulative values for GPS path
let currentLat = 37.5000;
let currentLong = 127.0000;
let timestampCount = 0;
let logHistory = [];
let chartInstance = null;

// Keep a history of telemetries for Replay Attack
let telemetryHistory = [];

// --- DOM Elements ---
const btnNormal = document.getElementById('btn-normal');
const attackButtons = document.querySelectorAll('.btn-attack');
const fheToggle = document.getElementById('fhe-toggle');
const mlModelRadios = document.querySelectorAll('input[name="ml-model"]');

const valSpeed = document.getElementById('val-speed');
const valSteering = document.getElementById('val-steering');
const valGps = document.getElementById('val-gps');

const threatBanner = document.getElementById('threat-banner');
const bannerIcon = document.getElementById('banner-icon');
const bannerText = document.getElementById('banner-text');

const fheProcessContainer = document.getElementById('fhe-process-container');
const fheStepLabel = document.getElementById('fhe-step-label');
const fheProgressFill = document.getElementById('fhe-progress-fill');
const logTableBody = document.getElementById('log-table-body');

const gaugeFill = document.getElementById('gauge-fill');
const gaugeVal = document.getElementById('gauge-val');
const gaugeStatus = document.getElementById('gauge-status');

const plainLatencyVal = document.getElementById('plain-latency-val');
const fheLatencyVal = document.getElementById('fhe-latency-val');
const overheadVal = document.getElementById('overhead-val');

// --- Event Listeners ---
btnNormal.addEventListener('click', () => setActiveAttack('none'));
attackButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const attackType = btn.getAttribute('data-attack');
        setActiveAttack(attackType);
    });
});

fheToggle.addEventListener('change', (e) => {
    fheEnabled = e.target.checked;
    updateConfigUI();
});

mlModelRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        selectedModel = e.target.value;
        updateLatencyDisplay();
    });
});

// --- UI Updates ---
function setActiveAttack(attack) {
    activeAttack = attack;
    
    // Reset button active classes
    if (attack === 'none') {
        btnNormal.classList.add('active');
        attackButtons.forEach(b => b.classList.remove('active'));
    } else {
        btnNormal.classList.remove('active');
        attackButtons.forEach(b => {
            if (b.getAttribute('data-attack') === attack) {
                b.classList.add('active');
            } else {
                b.classList.remove('active');
            }
        });
    }
}

function updateConfigUI() {
    if (fheEnabled) {
        fheProcessContainer.style.opacity = '1';
        fheProcessContainer.style.pointerEvents = 'auto';
    } else {
        fheProcessContainer.style.opacity = '0.3';
        fheProcessContainer.style.pointerEvents = 'none';
        fheStepLabel.textContent = "동형암호 미적용 (일반 전송)";
        fheProgressFill.style.width = '0%';
    }
}

function updateLatencyDisplay() {
    const data = LATENCY_DATA[selectedModel];
    plainLatencyVal.textContent = `${data.plain.toFixed(4)} ms`;
    fheLatencyVal.textContent = `${data.fhe.toFixed(2)} ms`;
    
    const overhead = (data.fhe / data.plain).toFixed(0);
    overheadVal.textContent = `~${Number(overhead).toLocaleString()}x`;
}

// --- Chart.js Setup ---
function initChart() {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'FHE Execution Time (ms)',
                    data: [],
                    borderColor: '#00b0ff',
                    backgroundColor: 'rgba(0, 176, 255, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Plaintext Time (ms)',
                    data: [],
                    borderColor: '#ff1744',
                    backgroundColor: 'rgba(255, 23, 68, 0.05)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    type: 'logarithmic',
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#90a4ae' }
                },
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#90a4ae' }
                }
            },
            plugins: {
                legend: { labels: { color: '#f0f4f8', font: { size: 10 } } }
            }
        }
    });
}

function updateChart(step, fheVal, plainVal) {
    if (!chartInstance) return;
    
    chartInstance.data.labels.push(step);
    chartInstance.data.datasets[0].data.push(fheVal);
    chartInstance.data.datasets[1].data.push(plainVal);
    
    // Keep last 10 items
    if (chartInstance.data.labels.length > 10) {
        chartInstance.data.labels.shift();
        chartInstance.data.datasets[0].data.shift();
        chartInstance.data.datasets[1].data.shift();
    }
    
    chartInstance.update('none'); // Update without animation for performance
}

// --- Main Simulation Loop ---
function runSimulationStep() {
    timestampCount++;
    
    // 1. Generate normal progressive state
    let speed = 40.0 + (Math.random() - 0.5) * 4.0; // fluctuation
    let steering = (Math.random() - 0.5) * 0.08;
    
    // GPS increments slowly
    currentLat += 0.0001 + (Math.random() - 0.5) * 0.00001;
    currentLong += 0.0001 + (Math.random() - 0.5) * 0.00001;
    
    let simulatedLat = currentLat;
    let simulatedLong = currentLong;
    
    // Save history for Replay Attack
    telemetryHistory.push({
        speed: speed,
        steering: steering,
        lat: simulatedLat,
        long: simulatedLong
    });
    if (telemetryHistory.length > 20) {
        telemetryHistory.shift();
    }
    
    // 2. Inject active cyber attack anomaly
    let isAttackInjected = activeAttack !== 'none';
    
    if (activeAttack === 'steering_takeover') {
        steering = Math.random() > 0.5 ? 1.0 : -1.0;
    } else if (activeAttack === 'gps_spoofing') {
        simulatedLat += 2.5 + Math.random();
        simulatedLong += 2.5 + Math.random();
    } else if (activeAttack === 'speed_jamming') {
        speed += 60.0 + Math.random() * 20;
    } else if (activeAttack === 'replay_attack') {
        // Playback older state from history
        const historicalIndex = Math.max(0, telemetryHistory.length - 10);
        const histData = telemetryHistory[historicalIndex] || { speed: 30.0, steering: 0.0, lat: currentLat, long: currentLong };
        speed = histData.speed;
        steering = histData.steering;
        simulatedLat = histData.lat;
        simulatedLong = histData.long;
    } else if (activeAttack === 'false_data_injection') {
        // Moderate constant biases
        speed += 25.0;
        steering += 0.35;
        simulatedLat += 0.25;
        simulatedLong += 0.25;
    } else if (activeAttack === 'dos_attack') {
        // Zero out data streams
        speed = 0.0;
        steering = 0.0;
        simulatedLat = 0.0;
        simulatedLong = 0.0;
    }
    
    // 3. UI update for current telemetry readings
    valSpeed.textContent = `${speed.toFixed(1)} km/h`;
    valSteering.textContent = `${steering.toFixed(4)} rad`;
    valGps.textContent = `${simulatedLat.toFixed(5)}, ${simulatedLong.toFixed(5)}`;
    
    // 4. ML Hacking Detector Classifier Logic (Threshold boundaries mimicking the AI model)
    let isDetected = false;
    
    // Checking standard boundaries to evaluate attack status
    if (Math.abs(steering) > 0.18) isDetected = true; // Steering anomaly
    if (speed > 55.0 || (speed < 10.0 && activeAttack === 'dos_attack')) isDetected = true; // Speed anomaly
    
    // GPS Spoofing / DoS anomaly
    const distanceLat = Math.abs(simulatedLat - currentLat);
    const distanceLong = Math.abs(simulatedLong - currentLong);
    if (distanceLat > 0.15 || distanceLong > 0.15 || simulatedLat === 0.0) {
        isDetected = true;
    }
    
    // Replay / sensor freeze anomaly
    if (activeAttack === 'replay_attack' && telemetryHistory.length > 5) {
        // In real AI, freeze over time is captured. Here we mark it detected.
        isDetected = true;
    }

    // 5. Run Detection Pipeline (FHE or Plaintext)
    const activeData = LATENCY_DATA[selectedModel];
    
    if (fheEnabled) {
        // Show FHE encryption/processing animation
        fheProcessContainer.classList.add('encrypting');
        fheStepLabel.textContent = "Encrypting Data (동형암호 변환 중)...";
        fheProgressFill.style.width = '30%';
        
        // Simulating FHE execution timeline
        setTimeout(() => {
            fheStepLabel.textContent = "Evaluating under Encryption (암호화 상태로 분석 중)...";
            fheProgressFill.style.width = '75%';
            
            setTimeout(() => {
                fheStepLabel.textContent = "Decrypting Results (결과 검증 및 복호화)...";
                fheProgressFill.style.width = '100%';
                
                setTimeout(() => {
                    // Complete pipeline
                    fheProcessContainer.classList.remove('encrypting');
                    fheStepLabel.textContent = "동형암호 상태로 안전하게 연산 완료";
                    
                    finalizeDetection(isDetected, speed, steering, simulatedLat, simulatedLong);
                    updateChart(timestampCount, activeData.fhe, activeData.plain);
                }, 100);
            }, activeData.fhe * 0.8);
        }, activeData.fhe * 0.2);
        
    } else {
        // Plaintext - instantaneous
        fheProgressFill.style.width = '0%';
        finalizeDetection(isDetected, speed, steering, simulatedLat, simulatedLong);
        updateChart(timestampCount, 0.01, activeData.plain);
    }
}

function finalizeDetection(isDetected, speed, steering, lat, long) {
    const timeStr = new Date().toLocaleTimeString();
    
    // Update threat banners
    if (isDetected) {
        threatBanner.className = "threat-banner alarm";
        bannerIcon.className = "fa-solid fa-triangle-exclamation";
        bannerText.textContent = `🚨 THREAT DETECTED: ${activeAttack.toUpperCase()} ATTACK!`;
        
        // Gauge update
        const randomCritical = 75 + Math.floor(Math.random() * 25);
        updateGauge(randomCritical, "CRITICAL", "var(--color-danger)");
        
    } else {
        threatBanner.className = "threat-banner safe";
        bannerIcon.className = "fa-solid fa-shield-halved";
        bannerText.textContent = "STATUS CLEAR: SECURED COMBAT PATROL";
        
        // Gauge update
        const randomSafe = 2 + Math.floor(Math.random() * 5);
        updateGauge(randomSafe, "SECURE", "var(--color-normal)");
    }
    
    // Add row to log table
    const resultBadge = isDetected 
        ? '<span class="badge badge-attack">ALERT</span>' 
        : '<span class="badge badge-normal">CLEAR</span>';
        
    const rowHTML = `
        <tr>
            <td>${timeStr}</td>
            <td>${speed.toFixed(1)} km/h</td>
            <td>${steering.toFixed(3)} rad</td>
            <td>${lat.toFixed(4)}, ${long.toFixed(4)}</td>
            <td>${resultBadge}</td>
        </tr>
    `;
    
    logTableBody.insertAdjacentHTML('afterbegin', rowHTML);
    
    // Keep max 8 logs
    if (logTableBody.children.length > 8) {
        logTableBody.lastElementChild.remove();
    }
}

function updateGauge(value, label, color) {
    gaugeVal.textContent = `${value}%`;
    gaugeStatus.textContent = label;
    gaugeStatus.style.color = color;
    
    // Rotate indicator: 0% = 0deg, 100% = 180deg
    const angle = (value / 100) * 180;
    gaugeFill.style.transform = `rotate(${angle}deg)`;
}

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    updateConfigUI();
    updateLatencyDisplay();
    updateGauge(4, "SECURE", "var(--color-normal)");
    
    // Start live simulation interval
    setInterval(runSimulationStep, 2000);
});
