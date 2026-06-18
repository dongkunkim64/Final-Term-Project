import paramiko
import time
import sys

def run_remote_carla_docker():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("1. 서버 접속 중...")
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        
        # 1. Docker 설치 여부 확인
        print("\n2. Docker 시스템 확인 중...")
        stdin, stdout, stderr = client.exec_command("which docker")
        docker_path = stdout.read().decode('utf-8').strip()
        
        if not docker_path:
            print("❌ Docker가 설치되어 있지 않습니다. 수동 설치가 필요합니다.")
            # 추가적으로 apt-get install docker.io 등을 스크립팅할 수 있지만 우선은 에러 처리
            return
        print(f"✅ Docker 설치 확인: {docker_path}")
        
        # 2. CARLA 도커 이미지 풀 및 실행 (0.9.14 버전)
        print("\n3. CARLA 시뮬레이터 (Docker 버전) 설치 및 백그라운드 실행 중...")
        print("   (주의: 이미지가 없을 경우 약 15GB 다운로드가 진행되므로 시간이 오래 걸릴 수 있습니다.)")
        
        # 기존에 돌고 있는 CARLA 컨테이너가 있다면 제거
        client.exec_command("docker rm -f carla-sim")
        
        # CARLA 도커 실행 (GPU 가속, 호스트 네트워크 사용, OffScreen 렌더링)
        # 다운로드가 오래 걸리므로 nohup으로 백그라운드에서 실행하고 로그를 남김
        run_cmd = (
            "nohup docker run --name carla-sim --net=host --gpus all -d "
            "carlasim/carla:0.9.14 /bin/bash -c './CarlaUE4.sh -RenderOffScreen' > carla_docker_install.log 2>&1 &"
        )
        client.exec_command(run_cmd)
        
        print("\n✅ CARLA 설치 및 구동 명령어가 백그라운드에 안전하게 전송되었습니다!")
        print("다운로드 및 압축 해제가 완료되면 시뮬레이터가 자동으로 켜질 것입니다.")
        print("설치 진행 상황은 서버의 'carla_docker_install.log' 파일에 기록되고 있습니다.")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        client.close()
        print("\n연결을 종료합니다.")

if __name__ == "__main__":
    run_remote_carla_docker()
