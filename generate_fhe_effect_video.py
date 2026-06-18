import cv2
import numpy as np
import time
import math

def generate_fhe_video():
    width, height = 1280, 720
    fps = 30
    duration = 10
    total_frames = fps * duration
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('fhe_effect_demonstration.mp4', fourcc, fps, (width, height))
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    print("FHE 효과 데몬스트레이션 영상 렌더링 시작...")
    
    for i in range(total_frames):
        # 배경 (Dark mode)
        frame = np.full((height, width, 3), (20, 20, 25), dtype=np.uint8)
        
        # 제목
        cv2.putText(frame, "FHE Logistic Regression Defense on UGV", (300, 50), font, 1.2, (255, 255, 255), 3)
        cv2.putText(frame, "Based on HCRL Car Hacking Dataset", (380, 90), font, 0.8, (200, 200, 200), 2)
        
        # UGV (Client) 박스 - 왼쪽
        cv2.rectangle(frame, (100, 200), (350, 600), (50, 50, 50), -1)
        cv2.rectangle(frame, (100, 200), (350, 600), (255, 255, 255), 2)
        cv2.putText(frame, "UGV (Client)", (150, 240), font, 1, (255, 255, 255), 2)
        
        # Cloud (Server) 박스 - 오른쪽
        cv2.rectangle(frame, (930, 200), (1180, 600), (50, 50, 50), -1)
        cv2.rectangle(frame, (930, 200), (1180, 600), (255, 255, 255), 2)
        cv2.putText(frame, "Cloud (Server)", (960, 240), font, 1, (255, 255, 255), 2)
        
        # 해커 (Hacker) 박스 - 하단 중앙
        if i > 90 and i < 180:
            cv2.rectangle(frame, (540, 550), (740, 650), (0, 0, 150), -1)
            cv2.rectangle(frame, (540, 550), (740, 650), (0, 0, 255), 2)
            cv2.putText(frame, "HACKER", (600, 590), font, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, "(RPM Spoofing)", (560, 620), font, 0.6, (255, 255, 255), 1)
            
            # 해커 화살표 (UGV쪽으로 데이터 주입)
            cv2.arrowedLine(frame, (540, 600), (360, 550), (0, 0, 255), 3, tipLength=0.1)
        
        # 시나리오 페이즈
        phase = ""
        speed = 50
        enc_data = "0x" + "".join([str(np.random.randint(0, 9)) for _ in range(8)])
        fhe_out = "0x" + "".join([str(np.random.randint(0, 9)) for _ in range(8)])
        latency = "2.47 ms"
        status = "SAFE"
        status_color = (0, 255, 0) # Green
        
        if i <= 90:
            phase = "1. Normal Driving"
            speed = 50 + int(math.sin(i/5) * 3)
            status = "SAFE (Normal Traffic)"
        elif i > 90 and i <= 180:
            phase = "2. Cyberattack Injected!"
            speed = 220 + (i % 10)
            status = "HACK DETECTED! (Braking)"
            status_color = (0, 0, 255) # Red
            
            # 배경 붉은 깜빡임 효과
            if (i // 5) % 2 == 0:
                frame = cv2.addWeighted(frame, 0.8, np.full((height, width, 3), (0, 0, 255), dtype=np.uint8), 0.2, 0)
        else:
            phase = "3. FHE Defense Active"
            speed = 0
            status = "FHE SECURED (Attack Blocked)"
            status_color = (255, 200, 0) # Cyan
        
        # 상태 텍스트
        cv2.putText(frame, phase, (500, 150), font, 1, (255, 255, 0), 2)
        
        # UGV 내부 데이터
        cv2.putText(frame, "Raw Sensor:", (120, 300), font, 0.7, (200, 200, 200), 1)
        cv2.putText(frame, f"Speed: {speed} km/h", (120, 330), font, 0.8, (255, 255, 255), 2)
        
        cv2.putText(frame, "FHE Encryption:", (120, 400), font, 0.7, (200, 200, 200), 1)
        cv2.putText(frame, f"E(X)={enc_data}", (120, 430), font, 0.6, (0, 255, 255), 2)
        
        # UGV -> Cloud 화살표 (암호문 전송)
        # 화살표에 떠다니는 암호문 효과
        arrow_x = 350 + (i * 15) % 580
        cv2.putText(frame, enc_data, (arrow_x, 330), font, 0.5, (0, 255, 255), 1)
        cv2.arrowedLine(frame, (350, 350), (930, 350), (150, 150, 150), 2, tipLength=0.03)
        cv2.putText(frame, "Send Encrypted Data", (550, 320), font, 0.6, (150, 150, 150), 1)
        
        # Cloud 내부 연산
        cv2.putText(frame, "FHE Inference:", (950, 300), font, 0.7, (200, 200, 200), 1)
        cv2.putText(frame, "Logistic Reg.", (950, 330), font, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "E(Y) = W*E(X) + B", (950, 370), font, 0.6, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Latency: {latency}", (950, 430), font, 0.8, (0, 255, 0), 2)
        
        # Cloud -> UGV 화살표 (결과 반환)
        arrow_x_ret = 930 - (i * 15) % 580
        cv2.putText(frame, fhe_out, (arrow_x_ret, 480), font, 0.5, (0, 255, 0), 1)
        cv2.arrowedLine(frame, (930, 500), (350, 500), (150, 150, 150), 2, tipLength=0.03)
        cv2.putText(frame, "Return Encrypted Result", (540, 470), font, 0.6, (150, 150, 150), 1)
        
        # UGV 복호화 및 판단
        cv2.putText(frame, "Decryption:", (120, 500), font, 0.7, (200, 200, 200), 1)
        cv2.putText(frame, f"Result: {status}", (120, 530), font, 0.7, status_color, 2)
        
        out.write(frame)

    out.release()
    print("FHE 효과 데몬스트레이션 영상(fhe_effect_demonstration.mp4) 렌더링 완료!")

if __name__ == '__main__':
    generate_fhe_video()
