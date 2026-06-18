import paramiko
import sys

def check_progress():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'
    
    total_size = 15858643801 # CARLA 0.9.14 tar.gz 바이트 수 (약 15.8GB)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=10)
        
        # 1. 파일 크기 확인 (다운로드 중인지)
        stdin, stdout, stderr = client.exec_command("stat -c%s /opt/CARLA_0.9.14.tar.gz 2>/dev/null")
        size_str = stdout.read().decode('utf-8').strip()
        
        # 2. 압축 해제 중인지 확인
        stdin2, stdout2, stderr2 = client.exec_command("tail -n 1 /root/carla_install.log")
        log_last_line = stdout2.read().decode('utf-8').strip()
        
        # 3. CARLA 구동 중인지 확인
        stdin3, stdout3, stderr3 = client.exec_command("ps aux | grep CarlaUE4 | grep -v grep")
        carla_proc = stdout3.read().decode('utf-8').strip()
        
        if carla_proc:
            print("100% 설치완료야. 남은 작업은 [데이터 및 영상 추출 스크립트 실행]이다.")
        elif "[2/3] Extracting CARLA" in log_last_line:
            print("95% 설치완료야. 남은 작업은 [CARLA 압축 해제 및 시뮬레이터 최초 구동]이다.")
        elif size_str and size_str.isdigit():
            current_size = int(size_str)
            percent = (current_size / total_size) * 100
            # 만약 100%가 넘거나 다 받아졌는데 아직 압축해제로 안 넘어갔다면
            if percent >= 99.9:
                percent = 99.9
            
            # 다운로드 속도 확인을 위해 현재 용량도 표기
            current_gb = current_size / (1024**3)
            total_gb = total_size / (1024**3)
            print(f"{percent:.1f}% 설치완료야. ({current_gb:.1f}GB / {total_gb:.1f}GB) 남은 작업은 [15GB 파일 다운로드 완료 및 압축 해제]이다.")
        else:
            print("0.0% 설치완료야. 남은 작업은 [다운로드 시작 대기]이다.")
            
    except Exception as e:
        print(f"상태 확인 중 오류 발생: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    check_progress()
