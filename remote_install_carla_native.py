import paramiko
import time

def run_native_carla_install():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        
        # 기존에 실패한 파일 삭제 및 curl을 이용해 리다이렉트 추적 다운로드 시작
        install_cmd = (
            "nohup bash -c '"
            "mkdir -p /opt/carla && "
            "cd /opt && "
            "rm -f CARLA_0.9.14.tar.gz && "
            "echo \"[1/3] Downloading CARLA (15GB)...\" && "
            "curl -L -o CARLA_0.9.14.tar.gz \"https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.14.tar.gz\" && "
            "echo \"[2/3] Extracting CARLA...\" && "
            "tar -xzf CARLA_0.9.14.tar.gz -C /opt/carla && "
            "echo \"[3/3] Starting CARLA Simulator...\" && "
            "cd /opt/carla && "
            "./CarlaUE4.sh -RenderOffScreen"
            "' > /root/carla_install.log 2>&1 &"
        )
        
        client.exec_command(install_cmd)
        
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_native_carla_install()
