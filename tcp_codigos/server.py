import socket

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 10379      # <-- Replace with the last 5 digits of your Student ID or DNI

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if data:
                print(f"Received: {data.decode()}")
                conn.sendall(b'Hello, Client!')

if __name__ == "__main__":
    start_server()
