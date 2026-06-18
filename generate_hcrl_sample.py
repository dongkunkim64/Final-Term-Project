import pandas as pd
import numpy as np
import time

def generate_hcrl_mock():
    np.random.seed(42)
    n_samples = 50000
    
    # 정상(R) 4만 개, 공격(T) 1만 개 (RPM/Gear Spoofing)
    n_normal = 40000
    n_attack = 10000
    
    timestamps = np.linspace(1513700000.0, 1513705000.0, n_samples)
    
    # CAN ID: 정상 주행 시 자주 등장하는 ID들
    normal_ids = ['0316', '018F', '0260', '02A0', '0329']
    
    data = []
    
    # 정상 데이터 생성
    for _ in range(n_normal):
        can_id = np.random.choice(normal_ids)
        # 정상 데이터 페이로드 (임의의 16진수 값들)
        payload = [np.random.randint(0, 255) for _ in range(8)]
        data.append([can_id, 8] + payload + ['R'])
        
    # 공격 데이터 생성 (예: 특정 ID에 대한 Spoofing 또는 DoS(0000))
    for _ in range(n_attack):
        attack_type = np.random.choice(['DoS', 'Fuzzy', 'Spoofing'])
        if attack_type == 'DoS':
            can_id = '0000'
            payload = [0, 0, 0, 0, 0, 0, 0, 0]
        elif attack_type == 'Fuzzy':
            can_id = f"{np.random.randint(0, 4095):04X}"
            payload = [np.random.randint(0, 255) for _ in range(8)]
        else: # Spoofing (RPM 조작)
            can_id = '0316'
            payload = [np.random.randint(200, 255) for _ in range(8)] # 비정상적으로 높은 값
            
        data.append([can_id, 8] + payload + ['T'])
        
    df = pd.DataFrame(data, columns=['CAN_ID', 'DLC', 'DATA_0', 'DATA_1', 'DATA_2', 'DATA_3', 'DATA_4', 'DATA_5', 'DATA_6', 'DATA_7', 'Flag'])
    df['Timestamp'] = timestamps
    
    # 컬럼 순서 재배치
    cols = ['Timestamp', 'CAN_ID', 'DLC', 'DATA_0', 'DATA_1', 'DATA_2', 'DATA_3', 'DATA_4', 'DATA_5', 'DATA_6', 'DATA_7', 'Flag']
    df = df[cols]
    
    # 셔플
    df = df.sample(frac=1).reset_index(drop=True)
    
    df.to_csv('HCRL_Car_Hacking_Sample.csv', index=False)
    print("고려대 HCRL 'Car Hacking Dataset' 포맷의 샘플 데이터(5만 건) 생성 완료: HCRL_Car_Hacking_Sample.csv")

if __name__ == '__main__':
    generate_hcrl_mock()
