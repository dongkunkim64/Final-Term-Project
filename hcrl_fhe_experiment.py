import pandas as pd
import numpy as np
import time
import tenseal as ts
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

def run_hcrl_experiment():
    print("1. HCRL Car Hacking Dataset 로드 중...")
    try:
        df = pd.read_csv('HCRL_Car_Hacking_Sample.csv')
    except:
        print("데이터셋 파일이 없습니다. 먼저 generate_hcrl_sample.py를 실행하세요.")
        return
        
    # 특성 추출 (DATA_0 ~ DATA_7)
    # CAN ID는 단순화를 위해 길이 또는 숫자형태로 변환하거나 드롭 (여기서는 DATA 값 8개만 피처로 사용)
    X = df[['DATA_0', 'DATA_1', 'DATA_2', 'DATA_3', 'DATA_4', 'DATA_5', 'DATA_6', 'DATA_7']].values
    
    # 정규화 (0~1)
    X = X / 255.0
    
    # 라벨링 (R -> 0: 정상, T -> 1: 해킹)
    y = np.where(df['Flag'] == 'T', 1, 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("2. 로지스틱 회귀 모델(평문) 학습 중...")
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train, y_train)
    
    plain_preds = lr_model.predict(X_test)
    plain_acc = accuracy_score(y_test, plain_preds)
    print(f"   -> 평문(Plaintext) 모델 정확도: {plain_acc*100:.2f}%")
    
    print("\n3. TenSEAL 동형암호(FHE) 컨텍스트 생성 중...")
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.global_scale = 2**40
    context.generate_galois_keys()
    
    # 학습된 LR 가중치를 FHE 모델로 변환
    weights = lr_model.coef_[0]
    bias = lr_model.intercept_[0]
    
    # 시그모이드 근사 함수 (y = 0.5 + 0.197*x - 0.004*x^3) -> 여기서는 연산량 최소화를 위해 선형 결합 부호만 판단
    print("4. FHE 기반 암호문 추론 테스트 (100건 샘플)...")
    
    fhe_preds = []
    latencies = []
    
    # 시간 관계상 100건만 테스트
    test_size = 100
    X_test_sample = X_test[:test_size]
    y_test_sample = y_test[:test_size]
    
    for i in range(test_size):
        # 1. 차량: 센서 데이터 암호화 (Client)
        enc_x = ts.ckks_vector(context, X_test_sample[i])
        
        # 2. 클라우드: 암호문 상태로 로지스틱 회귀 선형 결합 (Server)
        start_time = time.time()
        enc_out = enc_x.dot(weights) + bias
        # 클라우드 연산 시간 측정
        end_time = time.time()
        latencies.append((end_time - start_time) * 1000) # ms 변환
        
        # 3. 차량: 암호문 수신 및 복호화 후 판단 (Client)
        out = enc_out.decrypt()[0]
        fhe_preds.append(1 if out > 0 else 0)
        
    fhe_acc = accuracy_score(y_test_sample, fhe_preds)
    avg_latency = np.mean(latencies)
    
    print(f"   -> FHE 암호문 모델 정확도: {fhe_acc*100:.2f}%")
    print(f"   -> FHE 평균 추론 지연시간(Latency): {avg_latency:.2f} ms")
    
    # 결과 시각화
    plt.figure(figsize=(10, 5))
    
    # 왼쪽: 정확도 비교
    plt.subplot(1, 2, 1)
    bars = plt.bar(['Plaintext', 'FHE (Encrypted)'], [plain_acc*100, fhe_acc*100], color=['gray', 'blue'])
    plt.ylabel('Accuracy (%)')
    plt.title('Detection Accuracy Comparison')
    plt.ylim(0, 110)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f'{yval:.1f}%', ha='center', va='bottom')
        
    # 오른쪽: 평균 레이턴시
    plt.subplot(1, 2, 2)
    plt.bar(['FHE Inference\n(Logistic Reg)'], [avg_latency], color='green')
    plt.ylabel('Latency (ms)')
    plt.title('Average Inference Latency')
    plt.ylim(0, max(50, avg_latency + 10))
    plt.axhline(y=34.4, color='r', linestyle='--', label='Target (34.4ms)')
    plt.text(0, avg_latency + 1, f'{avg_latency:.1f} ms', ha='center', va='bottom', fontweight='bold')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('fhe_hcrl_validation.png')
    print("\n[SUCCESS] 검증 결과 그래프 'fhe_hcrl_validation.png' 저장 완료!")

if __name__ == '__main__':
    run_hcrl_experiment()
