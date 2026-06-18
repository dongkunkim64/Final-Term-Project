import cv2
import sys

def extract_poster():
    video_path = 'fhe_effect_demonstration.mp4'
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("비디오를 열 수 없습니다.")
        sys.exit(1)
        
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('poster.png', frame)
        print("poster.png 추출 완료!")
    else:
        print("프레임을 읽어올 수 없습니다.")
        
    cap.release()

if __name__ == '__main__':
    extract_poster()
