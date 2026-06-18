import paramiko
import time

def install_docker():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        print("Connected to server.")
        
        # Install Docker
        print("Installing docker...")
        stdin, stdout, stderr = client.exec_command("apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io", get_pty=True)
        print(stdout.read().decode())
        
        # Start CARLA
        print("Pulling and running CARLA...")
        stdin, stdout, stderr = client.exec_command("systemctl start docker && docker run -d --name carla_sim --net=host carlasim/carla:0.9.14 /bin/bash -c './CarlaUE4.sh -RenderOffScreen -nosound'", get_pty=True)
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Verify
        stdin, stdout, stderr = client.exec_command("docker ps")
        print("=== Docker PS ===")
        print(stdout.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    install_docker()
