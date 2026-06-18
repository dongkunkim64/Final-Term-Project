import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# 시계열 데이터 생성 (총 60초)
time_array = np.linspace(0, 60, 300)  # 300프레임
speed = np.zeros_like(time_array)
steering = np.zeros_like(time_array)

for i, t in enumerate(time_array):
    if t < 40:
        speed[i] = 50 + np.random.normal(0, 2)
        steering[i] = np.random.normal(0, 0.05)
    elif 40 <= t < 42:
        speed[i] = speed[i-1] + 1.5 + np.random.normal(0, 1)  # 급가속
        steering[i] = 0.8 + np.random.normal(0, 0.05)        # 급조향
    else:
        if speed[i-1] > 0:
            speed[i] = speed[i-1] - 4 + np.random.normal(0, 0.5)
            if speed[i] < 0: speed[i] = 0
        else:
            speed[i] = 0
        steering[i] = steering[i-1] * 0.8 + np.random.normal(0, 0.02)
        if abs(steering[i]) < 0.05:
            steering[i] = np.random.normal(0, 0.01)

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlim(0, 60)
ax1.set_ylim(0, 100)
ax1.set_xlabel('Time (Seconds)', fontweight='bold', fontsize=12)
ax1.set_ylabel('Speed (km/h)', color='tab:blue', fontweight='bold', fontsize=12)
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylim(-1, 1)
ax2.set_ylabel('Steering Angle', color='tab:orange', fontweight='bold', fontsize=12)
ax2.tick_params(axis='y', labelcolor='tab:orange')

line1, = ax1.plot([], [], color='tab:blue', linewidth=3, label='Speed')
line2, = ax2.plot([], [], color='tab:orange', linewidth=3, linestyle='--', label='Steering Angle')

# 주석 (텍스트 박스)
warning_text = ax1.text(30, 80, '', fontsize=18, fontweight='bold', color='white', 
                        bbox=dict(facecolor='red', alpha=0, edgecolor='none'),
                        horizontalalignment='center')

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    warning_text.set_text('')
    ax1.set_facecolor('white')
    return line1, line2, warning_text

def update(frame):
    t = time_array[frame]
    line1.set_data(time_array[:frame+1], speed[:frame+1])
    line2.set_data(time_array[:frame+1], steering[:frame+1])
    
    # 동적 배경색 및 깜빡임 효과
    if t < 40:
        ax1.set_facecolor('#f4f9f9')  # 부드러운 푸른/흰색 (정상)
        warning_text.set_text('System: NORMAL DRIVE')
        warning_text.set_bbox(dict(facecolor='blue', alpha=0.5, edgecolor='none'))
    elif 40 <= t < 42:
        # 해킹 발생: 화면이 붉은색으로 번쩍거림 (프레임 짝홀수 교차)
        if frame % 4 < 2:
            ax1.set_facecolor('#ffebee')  # 연한 붉은색
            warning_text.set_bbox(dict(facecolor='red', alpha=0.8, edgecolor='none'))
        else:
            ax1.set_facecolor('#ffcdd2')  # 진한 붉은색
            warning_text.set_bbox(dict(facecolor='darkred', alpha=0.9, edgecolor='none'))
        warning_text.set_text('!!! HACKING INTRUSION DETECTED !!!')
        warning_text.set_color('white')
        
    else:
        # FHE 제어: 초록색 안정화
        ax1.set_facecolor('#e8f5e9')  # 연한 초록색
        warning_text.set_text('FHE AI: SYSTEM SECURED (Brakes Applied)')
        warning_text.set_bbox(dict(facecolor='green', alpha=0.7, edgecolor='none'))
        
    return line1, line2, warning_text

# 애니메이션 생성
ani = animation.FuncAnimation(fig, update, frames=len(time_array), init_func=init, blit=True, interval=50)

print("동적 시계열 그래프 GIF 렌더링 시작...")
ani.save('glowsai_animated_graph.gif', writer='pillow', fps=20)
print("GIF 저장 완료: glowsai_animated_graph.gif")
