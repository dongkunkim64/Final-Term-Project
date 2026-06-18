import paramiko

def check():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        stdin, stdout, stderr = client.exec_command("docker ps -a")
        print("=== Docker PS ===")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = client.exec_command("docker logs --tail 20 carla_sim")
        print("=== CARLA Logs ===")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    check()
