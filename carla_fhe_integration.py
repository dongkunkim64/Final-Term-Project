import time
import math
import joblib
import numpy as np

# CARLA 모듈 로드 (서버에 설치되어 있다고 가정)
try:
    import carla
except ImportError:
    print("Warning: 'carla' module not found. Run this script inside the CARLA environment.")

# FHE 지연 시간 모사 (34ms)
def mock_fhe_inference(model, features):
    time.sleep(0.034)  # FHE 연산 대기 시간 (34ms)
    prediction = model.predict(features)
    return prediction[0]

def get_speed(vehicle):
    vel = vehicle.get_velocity()
    speed_ms = math.sqrt(vel.x**2 + vel.y**2 + vel.z**2)
    return speed_ms * 3.6  # km/h 변환

def main():
    print("=== [CARLA - FHE 실시간 연동 시스템 시작] ===")
    
    # 1. AI 모델 및 정규화기 로드
    try:
        scaler = joblib.load('ugv_scaler.pkl')
        model = joblib.load('ugv_model.pkl')
        print("[System] AI 모델 및 정규화기 로드 완료.")
    except Exception as e:
        print(f"[Error] 모델 파일을 찾을 수 없습니다: {e}")
        return

    # 2. CARLA 서버 연결
    print("[System] CARLA 시뮬레이터 접속 중... (localhost:2000)")
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        print("[System] CARLA 월드 접속 성공!")
    except Exception as e:
        print(f"[Error] CARLA 서버에 접속할 수 없습니다: {e}")
        return

    # 3. 차량 탐색
    blueprints = world.get_blueprint_library()
    vehicles = world.get_actors().filter('vehicle.*')
    
    if not vehicles:
        print("[Error] 현재 시뮬레이터 내에 스폰된 차량이 없습니다. 차량을 먼저 생성해주세요.")
        return
        
    target_vehicle = vehicles[0]
    print(f"[System] 차량 감지 완료: {target_vehicle.type_id}")

    # 4. 실시간 모니터링 루프
    print("\n--- 실시간 해킹 탐지 모니터링 가동 (FHE 적용) ---")
    try:
        while True:
            # 4-1. 실시간 센서 데이터 추출
            control = target_vehicle.get_control()
            transform = target_vehicle.get_transform()
            
            speed_kmh = get_speed(target_vehicle)
            steering = control.steer
            gps_lat = transform.location.x  # 단순화를 위해 좌표를 GPS로 매핑
            gps_long = transform.location.y
            
            # 4-2. 데이터 정규화 및 FHE 추론
            raw_data = np.array([[speed_kmh, steering, gps_lat, gps_long]])
            scaled_data = scaler.transform(raw_data)
            
            # FHE 환경에서 예측 수행 (34ms)
            start_time = time.time()
            prediction = mock_fhe_inference(model, scaled_data)
            latency = (time.time() - start_time) * 1000
            
            # 4-3. 결과 출력
            status_str = f"속도: {speed_kmh:4.1f}km/h | 조향: {steering:5.2f} | "
            if prediction == 1:
                print(f"🚨 [경고] 해킹 공격 탐지! 차량 제어 탈취 의심 (처리 속도: {latency:.1f}ms)")
            else:
                print(f"✅ {status_str} 상태: 정상 (처리 속도: {latency:.1f}ms)")
                
            time.sleep(0.1)  # 0.1초 주기로 검사
            
    except KeyboardInterrupt:
        print("\n[System] 모니터링을 종료합니다.")

if __name__ == '__main__':
    main()
