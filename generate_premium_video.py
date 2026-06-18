import cv2
import numpy as np
import math
import time

def add_hud(img, frame, phase):
    h, w = img.shape[:2]
    overlay = img.copy()
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    
    # 기본 변수
    speed = 50
    gps_lat = 34.0522
    gps_lon = -118.2437
    heading = 188
    status = "DRIVING"
    status_col = (255, 255, 255)
    mode = "AUTON"
    
    # 페이즈별 변화
    if phase == "NORMAL":
        speed = 50 + int(math.sin(frame/10)*2)
        gps_lat += frame * 0.0001
        gps_lon -= frame * 0.0001
    elif phase == "HACKED":
        speed = 85 + (frame % 5)
        heading = 188 - ((frame - 120) * 2)
        status = "WARNING! HACKED!"
        status_col = (0, 0, 255)
        mode = "MANUAL OVERRIDE"
    elif phase == "SECURED":
        speed = 0
        status = "FHE SECURED (BRAKED)"
        status_col = (0, 255, 0)
        
    # REC 깜빡임
    if (frame // 15) % 2 == 0:
        cv2.circle(overlay, (40, 45), 8, (0, 0, 255), -1)
    cv2.putText(overlay, "REC", (55, 50), font, 0.7, color, 2)
    
    # 좌상단
    cv2.putText(overlay, f"GPS: {gps_lat:.4f} N, {abs(gps_lon):.4f} W", (30, 80), font, 0.6, color, 2)
    cv2.putText(overlay, "ALT: 184m", (30, 110), font, 0.6, color, 2)
    
    # 우상단
    cv2.putText(overlay, f"VEL: {speed} KM/H", (w - 220, 50), font, 0.6, color, 2)
    cv2.putText(overlay, f"HEAD: {heading} S", (w - 220, 80), font, 0.6, color, 2)
    cv2.putText(overlay, "CAM: FLIR/EOP", (w - 220, 110), font, 0.6, color, 2)
    
    # 좌하단
    cv2.putText(overlay, f"MODE: {mode}", (30, h - 90), font, 0.6, color, 2)
    cv2.putText(overlay, f"STATUS: {status}", (30, h - 60), font, 0.7, status_col, 2)
    if phase == "HACKED":
        cv2.putText(overlay, "LATENCY: N/A", (30, h - 30), font, 0.6, color, 2)
    elif phase == "SECURED":
        cv2.putText(overlay, "FHE LATENCY: 34.4 ms", (30, h - 30), font, 0.7, (0, 255, 0), 2)
    
    # 우하단
    cv2.putText(overlay, "BATT: 88%", (w - 220, h - 90), font, 0.6, color, 2)
    cv2.putText(overlay, "SIGNAL: STRONG", (w - 220, h - 60), font, 0.6, color, 2)
    cv2.putText(overlay, "DIST: 1.4 KM", (w - 220, h - 30), font, 0.6, color, 2)
    
    # 크로스헤어
    cx, cy = w//2, h//2
    cv2.line(overlay, (cx-20, cy), (cx+20, cy), color, 1)
    cv2.line(overlay, (cx, cy-20), (cx, cy+20), color, 1)

    return overlay

def generate_video():
    img_normal = cv2.imread('/Users/dongkun/.gemini/antigravity/brain/4105df2d-6e8f-4271-a56d-b435de9b33c7/carla_normal_1781811948703.png')
    img_hacked = cv2.imread('/Users/dongkun/.gemini/antigravity/brain/4105df2d-6e8f-4271-a56d-b435de9b33c7/carla_hacked_1781811960077.png')
    img_secured = cv2.imread('/Users/dongkun/.gemini/antigravity/brain/4105df2d-6e8f-4271-a56d-b435de9b33c7/carla_secured_1781811973584.png')
    
    # 해상도 1280x720 통일
    size = (1280, 720)
    img_normal = cv2.resize(img_normal, size)
    img_hacked = cv2.resize(img_hacked, size)
    img_secured = cv2.resize(img_secured, size)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('carla_premium_3d_simulation.mp4', fourcc, 30.0, size)
    
    red_overlay = np.full((720, 1280, 3), (0, 0, 255), dtype=np.uint8)
    green_overlay = np.full((720, 1280, 3), (0, 255, 0), dtype=np.uint8)
    
    print("프리미엄 3D 시뮬레이션 영상 렌더링 시작...")
    
    # 0~4초 (120 프레임): 정상 주행 (줌 인 효과)
    for i in range(120):
        # 줌 인 효과 계산
        scale = 1 + (i * 0.0005)
        M = cv2.getRotationMatrix2D((640, 360), 0, scale)
        zoomed = cv2.warpAffine(img_normal, M, size)
        
        frame = add_hud(zoomed, i, "NORMAL")
        out.write(frame)
        
    # 4~6초 (60 프레임): 해킹 (카메라 쉐이크 및 붉은 깜빡임)
    for i in range(120, 180):
        dx = np.random.randint(-15, 15)
        dy = np.random.randint(-15, 15)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        shaken = cv2.warpAffine(img_hacked, M, size)
        
        # 붉은 경고 번쩍임
        if (i // 5) % 2 == 0:
            shaken = cv2.addWeighted(shaken, 0.8, red_overlay, 0.2, 0)
            
        frame = add_hud(shaken, i, "HACKED")
        out.write(frame)
        
    # 6~10초 (120 프레임): FHE 방어 (제동 충격 후 안정)
    for i in range(180, 300):
        # 초반 제동 충격
        if i < 190:
            dy = int(10 * math.cos((i-180)*0.5))
            M = np.float32([[1, 0, 0], [0, 1, dy]])
            stable = cv2.warpAffine(img_secured, M, size)
        else:
            stable = img_secured.copy()
            
        # 초록색 안정 틴트
        stable = cv2.addWeighted(stable, 0.9, green_overlay, 0.1, 0)
            
        frame = add_hud(stable, i, "SECURED")
        out.write(frame)

    out.release()
    print("프리미엄 영상(carla_premium_3d_simulation.mp4) 렌더링 완료!")

if __name__ == '__main__':
    generate_video()
