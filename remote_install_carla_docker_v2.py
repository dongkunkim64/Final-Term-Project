import paramiko

def run_docker_carla_install():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("[System] Connecting to Glows.ai server...")
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        
        # Docker 설치 및 CARLA 도커 이미지 백그라운드 다운로드 & 실행
        # 기존 실패한 native 설치 찌꺼기 무시하고 가장 확실한 Docker로 전환
        install_cmd = (
            "nohup bash -c '"
            "echo \"[1/4] Installing Docker & NVIDIA Toolkit...\" > /root/carla_docker.log && "
            "apt-get update -y && apt-get install -y docker.io nvidia-container-toolkit && "
            "systemctl restart docker && "
            "echo \"[2/4] Downloading CARLA Docker Image (15GB)...\" >> /root/carla_docker.log && "
            "docker pull carlasim/carla:0.9.14 >> /root/carla_docker.log 2>&1 && "
            "echo \"[3/4] Starting CARLA Simulator Container...\" >> /root/carla_docker.log && "
            "docker rm -f carla_sim || true && "
            "docker run -d --name carla_sim --net=host --gpus all carlasim/carla:0.9.14 /bin/bash -c \"./CarlaUE4.sh -RenderOffScreen -nosound\" && "
            "echo \"[4/4] CARLA Simulation is running!\" >> /root/carla_docker.log"
            "' > /dev/null 2>&1 &"
        )
        
        print("[System] Executing Docker Installation Script in background...")
        client.exec_command(install_cmd)
        print("[System] Docker script successfully launched.")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_docker_carla_install()
