import socket
import time

# Server configuration
SERVER_HOST = '127.0.0.1'  # Localhost or actual server IP
SERVER_PORT = 10379        # <-- Same port as server

def start_client():
    time.sleep(1)  # Give server time to start
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")

        filename = 'rfc793.txt'  # <-- Make sure this file exists!
        with open(filename, 'rb') as f:
            data = f.read(1024)
            while data:
                client_socket.sendall(data)
                data = f.read(1024)
        print(f"File '{filename}' sent to server.")

if __name__ == "__main__":
    start_client()
