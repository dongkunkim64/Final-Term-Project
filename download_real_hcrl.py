import os
import sys

def download_dataset():
    print("==================================================")
    print("고려대학교 HCRL 'Car Hacking Dataset' 원본 다운로더")
    print("==================================================")
    print("원본 데이터셋은 수백 MB ~ 수 GB에 달하는 방대한 용량이며,")
    print("Kaggle(캐글) 계정 인증이 필요하여 자동 다운로드가 제한되어 있습니다.\n")
    
    print("[다운로드 방법 1: Kaggle API 사용 (추천)]")
    print("1. 캐글(kaggle.com)에 로그인 후 Account에서 'Create New API Token'을 눌러 kaggle.json을 다운받습니다.")
    print("2. 터미널에서 다음 명령어를 입력하세요:")
    print("   pip install kaggle")
    print("   kaggle datasets download -d mkashifn/car-hacking-dataset")
    print("   unzip car-hacking-dataset.zip\n")
    
    print("[다운로드 방법 2: 웹브라우저에서 직접 다운로드]")
    print("아래 링크를 복사하여 인터넷 창에 붙여넣기 하시면 즉시 다운로드가 시작됩니다.")
    print("👉 링크: https://www.kaggle.com/datasets/mkashifn/car-hacking-dataset/download?datasetVersionNumber=1\n")
    
    print("다운로드가 완료되면 폴더 안에 다음 파일들이 생깁니다:")
    print(" - DoS_dataset.csv (서비스 거부 공격)")
    print(" - Fuzzy_dataset.csv (퍼지 공격)")
    print(" - RPM_dataset.csv (RPM 속도 조작 공격 - ★본 프로젝트 메인 데이터)")
    print(" - gear_dataset.csv (기어 조작 공격)")
    
if __name__ == '__main__':
    download_dataset()
