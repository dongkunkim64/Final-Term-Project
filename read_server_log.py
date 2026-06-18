import paramiko

def read_log():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=15)
        stdin, stdout, stderr = client.exec_command("cat /root/carla_docker.log")
        print("=== carla_docker.log ===")
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # Check OS info
        stdin, stdout, stderr = client.exec_command("cat /etc/os-release")
        print("=== OS Release ===")
        print(stdout.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    read_log()
