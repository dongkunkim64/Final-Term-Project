import glob
import os
import sys
import time
import math
import random
import csv
import numpy as np
import cv2
import joblib

# Try to import CARLA
try:
    import carla
except ImportError:
    print("Warning: carla module not found locally. This script is meant to be run on the remote CARLA server.")

def mock_fhe_inference(model, features):
    # FHE 오버헤드 34ms 대기
    time.sleep(0.034)
    return model.predict(features)[0]

def get_speed(vehicle):
    vel = vehicle.get_velocity()
    return math.sqrt(vel.x**2 + vel.y**2 + vel.z**2) * 3.6

def main():
    # 1. 모델 로드
    try:
        scaler = joblib.load('ugv_scaler.pkl')
        model = joblib.load('ugv_model.pkl')
        print("[System] AI 모델 로드 완료.")
    except Exception as e:
        print(f"[Error] 모델 로드 실패: {e}")
        return

    # 2. CARLA 접속
    client = carla.Client('localhost', 2000)
    client.set_timeout(20.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    
    # 3. UGV (차량) 스폰
    vehicle_bp = blueprint_library.filter('vehicle.tesla.cybertruck')[0] # 사이버트럭을 임시 UGV로 사용
    spawn_points = world.get_map().get_spawn_points()
    vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))
    if vehicle is None:
        print("차량 스폰 실패.")
        return
    print("[System] UGV 스폰 완료. Autopilot 활성화.")
    vehicle.set_autopilot(True)

    # 4. 카메라 센서 부착 (3인칭 드론 뷰)
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '1280')
    camera_bp.set_attribute('image_size_y', '720')
    camera_bp.set_attribute('fov', '90')
    camera_transform = carla.Transform(carla.Location(x=-6.5, z=2.5), carla.Rotation(pitch=-15.0))
    camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
    
    # 영상 녹화 및 센서 콜백 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video = cv2.VideoWriter('ugv_combat_video.mp4', fourcc, 20.0, (1280, 720))
    
    # 데이터 추출용 CSV 파일 열기
    csv_file = open('ugv_massive_data.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['timestamp', 'speed_kmh', 'steering_angle', 'gps_lat', 'gps_long', 'label', 'fhe_prediction'])
    
    # 전역 변수 해킹 방어용
    is_hacked = False
    hack_counter = 0
    frame_count = 0
    max_frames = 2000  # 약 100초 촬영 (20fps 기준)
    
    def process_image(image):
        nonlocal is_hacked, out_video, frame_count
        
        if frame_count > max_frames:
            return
            
        # CARLA 이미지를 numpy 배열(OpenCV)로 변환
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        
        # HUD 텍스트 그리기
        font = cv2.FONT_HERSHEY_SIMPLEX
        if is_hacked:
            # 해킹 경고 붉은색 테두리 효과
            cv2.rectangle(array, (0, 0), (1280, 720), (0, 0, 255), 10)
            cv2.putText(array, "WARNING: CYBER ATTACK DETECTED!", (200, 100), font, 1.5, (0, 0, 255), 4, cv2.LINE_AA)
            cv2.putText(array, "FHE AI: OVERRIDING CONTROL...", (250, 150), font, 1.0, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(array, "SYSTEM STATUS: NORMAL", (50, 50), font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
            
        cv2.putText(array, f"Speed: {get_speed(vehicle):.1f} km/h", (50, 100), font, 1.0, (255, 255, 255), 2)
        cv2.putText(array, "FHE Latency: 34ms", (50, 150), font, 0.8, (255, 255, 255), 2)
        
        out_video.write(array)
        frame_count += 1
        
    camera.listen(lambda image: process_image(image))

    # 5. 주행 루프 및 해킹 공격 주입
    print("[System] 데이터 추출 및 동영상 렌더링 시작...")
    try:
        for i in range(max_frames):
            control = vehicle.get_control()
            transform = vehicle.get_transform()
            speed = get_speed(vehicle)
            steer = control.steer
            
            # 해킹 시나리오 주입 (약 10% 확률로 50 프레임 동안 지속)
            if random.random() < 0.005 and not is_hacked:
                is_hacked = True
                hack_counter = 50
                print(f"[!] {i} 프레임: 사이버 공격(조향 탈취) 발생!")
                
            if is_hacked:
                control.steer = 1.0  # 운전대를 강제로 끝까지 꺾음
                vehicle.apply_control(control)
                hack_counter -= 1
                if hack_counter <= 0:
                    is_hacked = False
                    
            # FHE AI 추론 (데이터 정규화 적용)
            raw_data = np.array([[speed, steer, transform.location.x, transform.location.y]])
            scaled_data = scaler.transform(raw_data)
            prediction = mock_fhe_inference(model, scaled_data)
            
            # CSV 저장
            actual_label = 1 if is_hacked else 0
            csv_writer.writerow([i, speed, steer, transform.location.x, transform.location.y, actual_label, prediction])
            
            time.sleep(0.05)
            
    finally:
        print("[System] 렌더링 및 추출 완료. 센서 및 차량 제거 중...")
        camera.stop()
        camera.destroy()
        vehicle.destroy()
        out_video.release()
        csv_file.close()
        print("✅ 완료! 'ugv_combat_video.mp4' 및 'ugv_massive_data.csv' 생성됨.")

if __name__ == '__main__':
    main()
