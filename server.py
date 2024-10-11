import socket
import threading

def handle_client(client_socket, address):
    print(f"[+] Connection from {address} established.")
    
    while True:
        try:
            command = input(f"Enter command to send to {address} (or type 'exit' to close): ")
            client_socket.send(command.encode('utf-8'))

            # If command is 'exit', break the loop and close the connection
            if command.lower() == 'exit':
                print(f"[-] Closing connection with {address}")
                break

            # Receive the result from the client
            result = client_socket.recv(4096).decode('utf-8')
            if not result:
                print(f"[-] Connection with {address} closed.")
                break
            print(f"Result from {address}:\n{result}")
        
        except (ConnectionResetError, BrokenPipeError):
            print(f"[-] Connection with {address} lost.")
            break
        except Exception as e:
            print(f"[!] Error handling {address}: {e}")
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("[*] Listening on 0.0.0.0:9999")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
