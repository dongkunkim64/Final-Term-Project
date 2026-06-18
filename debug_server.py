import paramiko
import sys

def debug_server():
    hostname = 'tw-07.access.glows.ai'
    port = 27507
    username = 'root'
    password = 'X3rz#nJRmgp4cf,]'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname, port=port, username=username, password=password, timeout=10)
        
        stdin, stdout, stderr = client.exec_command("ls -lh /opt")
        print("=== /opt 폴더 ===")
        print(stdout.read().decode('utf-8'))
        
        stdin2, stdout2, stderr2 = client.exec_command("cat /root/carla_install.log")
        print("=== /root/carla_install.log ===")
        print(stdout2.read().decode('utf-8'))
        print("Error log:", stderr2.read().decode('utf-8'))
            
    except Exception as e:
        print(f"상태 확인 중 오류 발생: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    debug_server()
