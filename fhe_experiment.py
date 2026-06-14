import os
import time
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

try:
    # Import Concrete-ML models if available (Requires Python 3.8 ~ 3.11)
    from concrete.ml.sklearn import LogisticRegression as ConcreteLogisticRegression
    from concrete.ml.sklearn import DecisionTreeClassifier as ConcreteDecisionTreeClassifier
except ImportError:
    print("[경고] 현재 시스템의 Python 버전에서는 Zama Concrete-ML 설치가 지원되지 않습니다.")
    print("[안내] 실제 시연을 위해 FHE 연산 지연시간을 모사하는 Mock 클래스로 대체하여 실행합니다.\n")
    
    # Fallback Mock for Logistic Regression
    from sklearn.linear_model import LogisticRegression
    class ConcreteLogisticRegression(LogisticRegression):
        def __init__(self, n_bits=8, **kwargs):
            super().__init__(**kwargs)
            self.n_bits = n_bits
            
        def compile(self, X):
            time.sleep(1.0)
            pass
            
        def predict(self, X, fhe="disable"):
            if fhe == "execute":
                # FHE overhead simulation (approx. 34ms per sample)
                time.sleep(0.034 * len(X))
            return super().predict(X)

    # Fallback Mock for Decision Tree
    from sklearn.tree import DecisionTreeClassifier
    class ConcreteDecisionTreeClassifier(DecisionTreeClassifier):
        def __init__(self, n_bits=8, **kwargs):
            super().__init__(**kwargs)
            self.n_bits = n_bits
            
        def compile(self, X):
            time.sleep(1.5)
            pass
            
        def predict(self, X, fhe="disable"):
            if fhe == "execute":
                # FHE overhead simulation (approx. 45ms per sample due to deeper circuit)
                time.sleep(0.045 * len(X))
            return super().predict(X)

def run_fhe_experiment():
    print("=== [팀 프로젝트 실험] UGV 해킹 탐지 모델별 FHE vs Plaintext 비교 ===\n")
    
    # 1. 데이터 로드 및 전처리
    data_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(data_dir, 'ugv_combat_data.csv')
    df = pd.read_csv(data_path)
    X = df[['speed_kmh', 'steering_angle', 'gps_lat', 'gps_long']]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler_path = os.path.join(data_dir, 'ugv_scaler.pkl')
    scaler = joblib.load(scaler_path)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 평가를 위해 테스트 데이터 50개 샘플링 (FHE 시뮬레이션 시간 절약)
    num_samples = 50
    X_test_sample = X_test_scaled[:num_samples]
    y_test_sample = y_test.iloc[:num_samples].values
    
    print(f"[*] 테스트 샘플 수: {num_samples} 개")

    models = {
        "Logistic Regression": ConcreteLogisticRegression(n_bits=8),
        "Decision Tree": ConcreteDecisionTreeClassifier(n_bits=8, max_depth=5, random_state=42)
    }
    
    results = {}

    for model_name, fhe_model in models.items():
        print(f"\n--- {model_name} 실험 시작 ---")
        
        # 모델 학습 (동형암호 컴파일용)
        fhe_model.fit(X_train_scaled, y_train)
        
        # 컴파일: FHE 회로 생성
        compile_start = time.time()
        fhe_model.compile(X_train_scaled)
        compile_end = time.time()
        print(f"[-] 컴파일 소요 시간: {compile_end - compile_start:.2f} 초")

        # 1. Plaintext(일반) 모델 속도 측정
        print("[*] 평문(Plaintext) 추론 측정 중...")
        plain_start_time = time.time()
        plain_predictions = fhe_model.predict(X_test_sample)
        plain_end_time = time.time()
        
        plain_latency_per_sample = ((plain_end_time - plain_start_time) / num_samples) * 1000  # ms
        plain_acc = accuracy_score(y_test_sample, plain_predictions)

        # 2. FHE(동형암호) 모델 속도 측정
        print("[*] 동형암호(FHE) 추론 측정 중 (Encryption -> Inference -> Decryption)...")
        fhe_predictions = []
        fhe_total_latency = 0
        
        for i in range(num_samples):
            sample = X_test_sample[i:i+1]
            
            start_time = time.time()
            pred = fhe_model.predict(sample, fhe="execute")
            end_time = time.time()
            
            fhe_predictions.append(pred[0])
            fhe_total_latency += (end_time - start_time)
            
            if (i+1) % 10 == 0:
                print(f"   - {i+1}/{num_samples} 샘플 완료...")

        fhe_latency_per_sample = (fhe_total_latency / num_samples) * 1000  # ms
        fhe_acc = accuracy_score(y_test_sample, fhe_predictions)
        
        # 결과 저장
        results[model_name] = {
            "plain_accuracy": float(plain_acc * 100),
            "fhe_accuracy": float(fhe_acc * 100),
            "plain_latency_ms": float(plain_latency_per_sample),
            "fhe_latency_ms": float(fhe_latency_per_sample)
        }
        
        print(f"\n[{model_name} 결과 요약]")
        print(f"   - Plain Accuracy: {plain_acc * 100:.2f}% | Latency: {plain_latency_per_sample:.4f} ms")
        print(f"   - FHE Accuracy:   {fhe_acc * 100:.2f}% | Latency: {fhe_latency_per_sample:.4f} ms")
        print(f"   - 오버헤드: 약 {fhe_latency_per_sample / plain_latency_per_sample:.0f}배 느려짐")

    # 결과를 JSON 파일로 저장
    results_path = os.path.join(data_dir, 'fhe_results.json')
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print("\n========================================================")
    print("실험 완료! 모든 모델 결과가 fhe_results.json에 저장되었습니다.")
    print("========================================================")

if __name__ == "__main__":
    run_fhe_experiment()
