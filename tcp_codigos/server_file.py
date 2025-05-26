import socket

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 10379      # <-- Replace with your last 5 digits of Student ID / DNI

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            with open('received_file.txt', 'wb') as f:  # Open a file to write the received data
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print("File received and saved as 'received_file.txt'")

if __name__ == "__main__":
    start_server()
