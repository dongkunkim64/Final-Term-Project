import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# 애니메이션 하이라이트 시나리오 (총 10초, 100프레임)
# 0~4초: 정상 직진
# 4~6초: 해킹 (급조향, 과속)
# 6~10초: FHE 제어 (급정거)

frames = 100
fps = 10

# 데이터 생성
x = np.zeros(frames)
y = np.zeros(frames)
speed = np.zeros(frames)
steering = np.zeros(frames)
status = ["NORMAL"] * frames
color = ["blue"] * frames

current_x = 0
current_y = 0
current_speed = 50
current_angle = 90  # 90 degrees is straight up

for i in range(frames):
    t = i / fps
    if t < 4:
        # 정상 주행
        current_speed = 50
        current_angle += np.random.normal(0, 0.5)
        status[i] = "NORMAL DRIVE"
        color[i] = "blue"
    elif 4 <= t < 6:
        # 해킹 발생
        current_speed += 3  # 과속
        current_angle -= 15  # 우측으로 급하게 꺾음
        status[i] = "!!! HACKING DETECTED !!!"
        color[i] = "red"
    else:
        # FHE 방어 (제동)
        if current_speed > 0:
            current_speed -= 8
            if current_speed < 0:
                current_speed = 0
        status[i] = "FHE SECURED (BRAKED)"
        color[i] = "green"
        
    speed[i] = current_speed
    steering[i] = current_angle
    
    # 위치 계산 (속도와 각도 기반 이동)
    rad = np.radians(current_angle)
    current_x += (current_speed / 10) * np.cos(rad)
    current_y += (current_speed / 10) * np.sin(rad)
    
    x[i] = current_x
    y[i] = current_y

# 애니메이션 설정
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-50, 150)
ax.set_ylim(-10, 300)
ax.set_facecolor('black')
ax.grid(True, color='gray', alpha=0.3)
ax.set_title("CARLA UGV Simulation - Radar View", color='white', fontweight='bold', pad=20)

# 차량을 나타내는 점
vehicle, = ax.plot([], [], 'o', markersize=15, color='cyan')
trajectory, = ax.plot([], [], '-', color='cyan', alpha=0.5, linewidth=2)

# HUD 텍스트
hud_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, color='white', 
                   fontsize=14, verticalalignment='top', fontweight='bold',
                   bbox=dict(facecolor='black', alpha=0.7, edgecolor='white'))

def init():
    vehicle.set_data([], [])
    trajectory.set_data([], [])
    hud_text.set_text('')
    return vehicle, trajectory, hud_text

def update(frame):
    # 경로 업데이트
    trajectory.set_data(x[:frame], y[:frame])
    # 현재 위치 업데이트
    vehicle.set_data([x[frame]], [y[frame]])
    vehicle.set_color(color[frame])
    trajectory.set_color(color[frame])
    
    # 배경 번쩍임 효과 (해킹 시)
    if color[frame] == "red":
        ax.set_facecolor((0.2, 0, 0))  # 어두운 붉은색
    elif color[frame] == "green":
        ax.set_facecolor((0, 0.2, 0))  # 어두운 초록색
    else:
        ax.set_facecolor('black')

    # HUD 정보 업데이트
    hud = (
        f"STATUS: {status[frame]}\n"
        f"SPEED: {speed[frame]:.1f} km/h\n"
        f"STEERING: {steering[frame]:.1f} deg\n"
        f"FHE LATENCY: 34.4 ms\n"
        f"TIME: {frame/fps:.1f} s"
    )
    hud_text.set_text(hud)
    hud_text.set_color(color[frame])
    
    return vehicle, trajectory, hud_text

ani = animation.FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=100)

print("GIF 애니메이션 렌더링 시작...")
ani.save('carla_ugv_simulation_video.gif', writer='pillow', fps=fps)
print("GIF 애니메이션(carla_ugv_simulation_video.gif) 생성 완료!")
