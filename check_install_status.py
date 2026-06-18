import paramiko
import sys

def check_status():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=10)
        
        # 로그 파일 마지막 15줄 확인
        stdin, stdout, stderr = client.exec_command("tail -n 15 /root/carla_install.log")
        out = stdout.read().decode('utf-8').strip()
        
        # CARLA 구동 여부 확인 (CarlaUE4 프로세스가 떠 있는지)
        stdin2, stdout2, stderr2 = client.exec_command("ps aux | grep CarlaUE4 | grep -v grep")
        carla_process = stdout2.read().decode('utf-8').strip()
        
        print("--- 📡 원격 서버 설치 현황 (실시간) ---")
        if out:
            print(out)
        else:
            print("로그 파일(/root/carla_install.log)이 아직 없거나 비어 있습니다.")
            
        print("\n--- 🏎️ CARLA 구동 여부 ---")
        if carla_process:
            print("✅ 성공: CARLA 시뮬레이터가 현재 구동 중입니다!")
        else:
            print("⏳ 대기: 아직 CARLA 시뮬레이터가 켜지지 않았습니다. (다운로드/압축해제 중)")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    check_status()
