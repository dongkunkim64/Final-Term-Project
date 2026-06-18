import carla
import cv2
import numpy as np
import time
import math
import argparse

def draw_hud(img, vehicle):
    # 차량 상태 정보 가져오기
    v = vehicle.get_velocity()
    speed_kmh = int(3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2))
    transform = vehicle.get_transform()
    heading = int(transform.rotation.yaw)
    loc = transform.location
    alt = int(loc.z)
    
    # 임의의 GPS 좌표 기반 (CARLA Location을 위경도로 매핑하는 가상 로직)
    gps_lat = 34.0522 + (loc.x / 111000.0)
    gps_lon = -118.2437 + (loc.y / 111000.0)

    # 폰트 설정
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    color = (255, 255, 255) # White
    red_color = (0, 0, 255) # Red for REC
    
    h, w = img.shape[:2]

    # --- Top Left ---
    # 깜빡이는 REC 버튼 효과
    blink = int(time.time() * 2) % 2 == 0
    if blink:
        cv2.circle(img, (40, 45), 8, red_color, -1)
    cv2.putText(img, "REC", (55, 50), font, font_scale+0.1, color, thickness)
    
    cv2.putText(img, f"GPS: {abs(gps_lat):.4f} {'N' if gps_lat>0 else 'S'}, {abs(gps_lon):.4f} {'E' if gps_lon>0 else 'W'}", (30, 80), font, font_scale, color, thickness)
    cv2.putText(img, f"ALT: {alt}m", (30, 110), font, font_scale, color, thickness)
    
    # --- Top Right ---
    cv2.putText(img, f"VEL: {speed_kmh} KM/H", (w - 220, 50), font, font_scale, color, thickness)
    cv2.putText(img, f"HEAD: {heading} DEG", (w - 220, 80), font, font_scale, color, thickness)
    cv2.putText(img, "CAM: FLIR/EOP", (w - 220, 110), font, font_scale, color, thickness)
    t = time.localtime()
    cv2.putText(img, f"TIME: {time.strftime('%H:%M:%S', t)}", (w - 220, 140), font, font_scale, color, thickness)

    # --- Bottom Left ---
    # 해킹/방어 상태에 따른 동적 표시
    status = "DRIVING"
    status_color = color
    if speed_kmh > 80:
        status = "WARNING! (HACKED)"
        status_color = (0, 0, 255)
    
    cv2.putText(img, "MODE: AUTON", (30, h - 90), font, font_scale, color, thickness)
    cv2.putText(img, f"STATUS: {status}", (30, h - 60), font, font_scale, status_color, thickness)
    cv2.putText(img, "OBST: NONE", (30, h - 30), font, font_scale, color, thickness)

    # --- Bottom Right ---
    cv2.putText(img, "BATT: 88%", (w - 220, h - 90), font, font_scale, color, thickness)
    cv2.putText(img, "SIGNAL: STRONG", (w - 220, h - 60), font, font_scale, color, thickness)
    cv2.putText(img, "DIST: 1.4 KM", (w - 220, h - 30), font, font_scale, color, thickness)
    
    # 중앙 조준점 (크로스헤어)
    cx, cy = w // 2, h // 2
    cv2.line(img, (cx - 20, cy), (cx + 20, cy), color, 1)
    cv2.line(img, (cx, cy - 20), (cx, cy + 20), color, 1)

    return img

def process_img(image, vehicle):
    # CARLA image to Numpy array
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    img = array[:, :, :3] # RGBA to RGB
    
    # HUD 오버레이 그리기
    img_hud = draw_hud(img, vehicle)
    
    cv2.imshow("CARLA Military UGV Dashcam View", img_hud)
    cv2.waitKey(1)

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    
    blueprint_library = world.get_blueprint_library()
    # UGV 역할로 군용/오프로드 차량 선택 (없으면 model3)
    vehicle_bp = blueprint_library.filter('vehicle.*')[0] 
    
    spawn_point = world.get_map().get_spawn_points()[0]
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    
    # 카메라 위치를 차량의 본넷/대시캠 위치로 조정 (X=앞, Z=높이)
    cam_bp = blueprint_library.find('sensor.camera.rgb')
    cam_bp.set_attribute('image_size_x', '1280')
    cam_bp.set_attribute('image_size_y', '720')
    cam_bp.set_attribute('fov', '90')
    cam_transform = carla.Transform(carla.Location(x=1.5, z=1.8))
    
    camera = world.spawn_actor(cam_bp, cam_transform, attach_to=vehicle)
    
    # 차량 자동주행 모드 켜기
    vehicle.set_autopilot(True)
    
    print("CARLA UGV HUD 카메라 실행 중... (종료하려면 화면 클릭 후 Q 또는 Ctrl+C)")
    
    try:
        # 카메라 센서 콜백에 HUD 렌더링 연결
        camera.listen(lambda image: process_img(image, vehicle))
        
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("종료 중... 센서와 차량을 삭제합니다.")
        camera.stop()
        camera.destroy()
        vehicle.destroy()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
