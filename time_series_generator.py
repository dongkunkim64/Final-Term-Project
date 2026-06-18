import matplotlib.pyplot as plt
import numpy as np

# 시계열 데이터 생성 (총 60초)
time = np.linspace(0, 60, 600)  # 0.1초 단위
speed = np.zeros_like(time)
steering = np.zeros_like(time)

# 시나리오 구성
# 0~40초: 정상 주행 (속도 약 50km/h, 조향각 0근처)
# 40~42초: 해킹 공격 발생 (가속 페달 풀, 핸들 확 꺾음)
# 42~60초: FHE AI가 0.034초만에 감지 후 제어권 회수 (브레이크 작동, 조향 원상복구)

for i, t in enumerate(time):
    if t < 40:
        # 정상
        speed[i] = 50 + np.random.normal(0, 2)
        steering[i] = np.random.normal(0, 0.05)
    elif 40 <= t < 42:
        # 해킹 발생 (급가속 및 급조향)
        speed[i] = speed[i-1] + 2.5 + np.random.normal(0, 1)  # 점점 치솟음
        steering[i] = 0.8 + np.random.normal(0, 0.05)
    else:
        # FHE 제어권 회수 후 급정거
        if speed[i-1] > 0:
            speed[i] = speed[i-1] - 4 + np.random.normal(0, 0.5)
            if speed[i] < 0:
                speed[i] = 0
        else:
            speed[i] = 0
        
        # 조향 원상 복구
        steering[i] = steering[i-1] * 0.8 + np.random.normal(0, 0.02)
        if abs(steering[i]) < 0.05:
            steering[i] = np.random.normal(0, 0.01)

fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Time (Seconds)', fontweight='bold')
ax1.set_ylabel('Speed (km/h)', color=color, fontweight='bold')
line1, = ax1.plot(time, speed, color=color, linewidth=2, label='Speed')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 100)

ax2 = ax1.twinx()  
color = 'tab:orange'
ax2.set_ylabel('Steering Angle', color=color, fontweight='bold')
line2, = ax2.plot(time, steering, color=color, linewidth=2, linestyle='--', label='Steering Angle')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(-1, 1)

# 해킹 이벤트 및 FHE 방어 구간 강조
ax1.axvspan(40, 42, color='red', alpha=0.3, label='Hacking Attack Detected!')
ax1.axvspan(42, 60, color='green', alpha=0.1, label='FHE AI Defense & Recovery')

# 주석 추가
ax1.annotate('Hacker Takes Control\n(Speed Spikes, Sharp Turn)', xy=(41, 80), xytext=(20, 85),
             arrowprops=dict(facecolor='red', shrink=0.05), fontsize=10, fontweight='bold', color='red')

ax1.annotate('FHE AI Intervenes (34ms)\n(Emergency Brake Applied)', xy=(42.5, 40), xytext=(45, 60),
             arrowprops=dict(facecolor='green', shrink=0.05), fontsize=10, fontweight='bold', color='green')

# 통합 범례
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

plt.title('Real-time UGV Data Flow: Normal Drive ➡️ Hacking Attack ➡️ FHE Defense', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()

plt.savefig('glowsai_time_series_flow.png', dpi=300)
print("시계열 데이터 흐름 차트(glowsai_time_series_flow.png) 생성 완료.")
