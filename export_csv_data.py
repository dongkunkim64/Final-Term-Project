import pandas as pd
import numpy as np

# 10만 개 데이터 생성
np.random.seed(42)

# 정상 8만 개, 해킹 2만 개
n_normal = 80000
n_hacked = 20000

normal_speed = np.random.normal(50, 5, n_normal)
normal_steering = np.random.normal(0, 0.1, n_normal)
normal_labels = np.zeros(n_normal, dtype=int)

hacked_speed = np.random.normal(85, 15, n_hacked)
hacked_steering = np.random.normal(0.8, 0.2, n_hacked)
hacked_labels = np.ones(n_hacked, dtype=int)

speed = np.concatenate([normal_speed, hacked_speed])
steering = np.concatenate([normal_steering, hacked_steering])
labels = np.concatenate([normal_labels, hacked_labels])

df = pd.DataFrame({
    'timestamp': pd.date_range(start='2026-06-18 10:00:00', periods=100000, freq='100L'),
    'speed_kmh': speed.round(2),
    'steering_angle': steering.round(3),
    'is_hacked': labels
})

# 셔플
df = df.sample(frac=1).reset_index(drop=True)

df.to_csv('glowsai_ugv_dataset_100k.csv', index=False)
print("10만 건 원시 데이터셋(glowsai_ugv_dataset_100k.csv) 추출 및 저장 완료!")
