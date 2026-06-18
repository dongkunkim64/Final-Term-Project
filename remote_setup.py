import paramiko
import sys
import time

def run_remote_commands():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("1. 서버 접속 중...")
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        
        print("\n2. GitHub 저장소 다운로드 (Clone/Pull)...")
        stdin, stdout, stderr = client.exec_command(
            "if [ -d 'Final-Term-Project' ]; then cd Final-Term-Project && git pull; else git clone https://github.com/dongkunkim64/Final-Term-Project.git; fi"
        )
        print(stdout.read().decode('utf-8').strip())
        print(stderr.read().decode('utf-8').strip())
        
        print("\n3. CARLA 시뮬레이터 설치 경로 검색 중 (시간이 조금 걸릴 수 있습니다)...")
        stdin, stdout, stderr = client.exec_command("find / -name CarlaUE4.sh -type f 2>/dev/null | head -n 1")
        carla_path = stdout.read().decode('utf-8').strip()
        
        if not carla_path:
            print("❌ CARLA 설치 경로를 찾을 수 없습니다. 서버에 CARLA가 설치되어 있는지 확인이 필요합니다.")
            return
            
        print(f"✅ CARLA 경로 발견: {carla_path}")
        
        print("\n4. CARLA 시뮬레이터 백그라운드 실행 (Off-Screen 모드)...")
        carla_dir = carla_path.rsplit('/', 1)[0]
        client.exec_command(f"cd {carla_dir} && nohup ./CarlaUE4.sh -RenderOffScreen > /dev/null 2>&1 &")
        
        print("CARLA가 부팅될 때까지 15초 대기합니다...")
        time.sleep(15)
        
        print("\n5. FHE 실시간 연동 스크립트 실행 (10초간 테스트)...")
        # 무한 루프 스크립트이므로 timeout 명령어로 10초만 실행하고 강제 종료합니다.
        stdin, stdout, stderr = client.exec_command(
            "cd Final-Term-Project && timeout 10 python3 carla_fhe_integration.py"
        )
        
        out = stdout.read().decode('utf-8').strip()
        err = stderr.read().decode('utf-8').strip()
        
        print("\n--- 🖥️ 서버 출력 결과 ---")
        if out: print(out)
        if err: print("\n[에러/경고]:\n" + err)
        
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        client.close()
        print("\n작업 완료, 연결을 종료합니다.")

if __name__ == "__main__":
    run_remote_commands()
