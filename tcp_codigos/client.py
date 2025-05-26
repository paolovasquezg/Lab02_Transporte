import socket
import time

# Server configuration
SERVER_HOST = '127.0.0.1'  # Use 127.0.0.1 for local, or actual IP if separate machines
SERVER_PORT = 10379        # <-- Same port as server

def start_client():
    time.sleep(1)  # Give server a little time to start
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")
        client_socket.sendall(b'Hello, Server!')
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

if __name__ == "__main__":
    start_client()
