import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. 시뮬레이션 데이터 생성 (이론적/경험적 FHE 벤치마크 기준)
# 로지스틱 회귀: 단일 선형 연산 (가장 낮음)
# 간단한 비선형 DNN (3-Layer MLP + ReLU 다항식 근사): 다항식 차수가 높아져 곱셈 횟수(Multiplicative Depth) 폭발
data = {
    'Model': ['Logistic Regression\n(Linear)', 'DNN - 3 Layers\n(Non-linear ReLU)', 'DNN - 5 Layers\n(Non-linear Sigmoid)'],
    'FHE_Latency_ms': [34.4, 850.2, 3420.5],
    'Multiplicative_Depth': [1, 5, 12],
    'Accuracy': [96.1, 97.5, 98.0]
}

df = pd.DataFrame(data)

# 2. 결과 표 (Table) Markdown 포맷으로 터미널 출력
print("=== [결과 표] FHE 환경에서의 비선형 함수 vs 선형 함수 성능 비교 ===")
print("| 모델 구조 (활성화 함수) | 정확도 (Accuracy) | FHE 곱셈 깊이 | 1회 추론 시간 (Latency) | 자율주행 적합성 |")
print("|---|---|---|---|---|")
for idx, row in df.iterrows():
    suitability = "✅ 통과 (실시간)" if row['FHE_Latency_ms'] < 100 else "❌ 불가 (사고위험)"
    model_name = row['Model'].replace('\n', ' ')
    print(f"| {model_name} | {row['Accuracy']}% | {row['Multiplicative_Depth']} | {row['FHE_Latency_ms']} ms | {suitability} |")

# 3. 상호 비교 그래프 생성 (Bar Chart)
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('AI Model Architecture')
ax1.set_ylabel('FHE Inference Latency (ms)', color=color, fontweight='bold', fontsize=12)
bars = ax1.bar(df['Model'], df['FHE_Latency_ms'], color=['#4caf50', '#ff9800', '#f44336'], width=0.5)
ax1.tick_params(axis='y', labelcolor=color)

# 100ms 자율주행 한계선 표시
ax1.axhline(y=100, color='r', linestyle='--', linewidth=2, label='100ms Limit (Autonomous Driving)')
ax1.legend(loc='upper left')

# 막대 위에 Latency 수치 텍스트 표시
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f'{yval} ms', ha='center', va='bottom', fontweight='bold')

# 정확도를 꺾은선 그래프로 추가 (이중 Y축)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Accuracy (%)', color=color, fontweight='bold', fontsize=12)
line = ax2.plot(df['Model'], df['Accuracy'], color=color, marker='o', linewidth=3, markersize=10, label='Accuracy')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(90, 100)

plt.title('FHE Latency vs Accuracy: Logistic Regression vs Non-linear DNNs', fontsize=14, fontweight='bold', pad=20)
fig.tight_layout()

# 4. 그래프 이미지 저장
save_path = 'fhe_latency_comparison.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"\n[System] 상호 비교 그래프가 '{save_path}' 로 저장되었습니다.")
