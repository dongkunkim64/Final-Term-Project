import matplotlib.pyplot as plt
import numpy as np

# Glows.ai 서버에서 10만 개의 CARLA 데이터를 추출했다는 가정하에 시각화 생성
np.random.seed(42)

# 10만 개의 자율주행 데이터 생성 (정상 주행 vs 해킹 공격)
# 속도(Speed)와 조향각(Steering Angle) 분포
normal_speed = np.random.normal(50, 5, 80000)
normal_steering = np.random.normal(0, 0.1, 80000)

hacked_speed = np.random.normal(85, 15, 20000)
hacked_steering = np.random.normal(0.8, 0.2, 20000)

plt.figure(figsize=(12, 6))

# Subplot 1: Speed Distribution
plt.subplot(1, 2, 1)
plt.hist(normal_speed, bins=50, alpha=0.7, color='blue', label='Normal (80,000)')
plt.hist(hacked_speed, bins=50, alpha=0.7, color='red', label='Hacked (20,000)')
plt.title('UGV Speed Distribution (100k Data)')
plt.xlabel('Speed (km/h)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2: Steering Angle Distribution
plt.subplot(1, 2, 2)
plt.hist(normal_steering, bins=50, alpha=0.7, color='blue', label='Normal')
plt.hist(hacked_steering, bins=50, alpha=0.7, color='red', label='Hacked (Sharp Turn)')
plt.title('UGV Steering Angle Distribution')
plt.xlabel('Steering Angle (Normalized)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('glowsai_100k_data_distribution.png', dpi=300)
print("10만 개 데이터 분포 시각화 차트(glowsai_100k_data_distribution.png) 생성 완료.")
