import paramiko
import sys

def test_ssh():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    try:
        print(f"Connecting to {username}@{hostname}:{port}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 접속 시도
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        print("✅ SSH Connection Successful!")
        
        # 시스템 정보 및 CARLA 실행 여부 확인
        commands = [
            "uname -a",                 # OS 정보
            "nvidia-smi",               # GPU 정보 (CARLA 서버는 보통 GPU를 씁니다)
            "ps aux | grep CarlaUE4"    # CARLA가 실행 중인지 확인
        ]
        
        print("\n--- 서버 상태 확인 시작 ---")
        for cmd in commands:
            print(f"\n> 실행 명령어: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode('utf-8').strip()
            if out:
                print(out)
                
        client.close()
        
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_ssh()
