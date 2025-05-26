import socket
import random
import hashlib

HOST = "0.0.0.0"
PORT = 9006
TIMEOUT = 10


# Corrupccion paquete, corrupcion del checksum
# Cambiar el puerto hace q el sender quede en bucle.

def is_corrupted():
    return random.random() < 0.5

class Receiver:
    def __init__(self, host, port):
        self.expected_seq = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))

    def compute_checksum(self, data):
        return hashlib.md5(data.encode()).hexdigest()

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()

            try:
                seq_str, recv_checksum, payload = message.split(":", 2)
                expected_checksum = self.compute_checksum(payload)

                if recv_checksum != expected_checksum:
                    print("[Receiver] Invalid checksum. Sending NAK.")
                    self.sock.sendto("NAK".encode(), addr)
                    continue

                seq = int(seq_str)

                if seq == self.expected_seq:
                    print(f"[Receiver] Received valid packet {seq}: {payload}")
                    self.sock.sendto("ACK".encode(), addr)
                    self.expected_seq += 1
                else:
                    print(f"[Receiver] Unexpected sequence {seq}. Sending NAK.")
                    self.sock.sendto("NAK".encode(), addr)

            except ValueError:
                print("[Receiver] Malformed packet. Sending NAK.")
                self.sock.sendto("NAK".encode(), addr)

def run_receiver():
    receiver = Receiver(HOST, PORT)
    receiver.listen()


run_receiver()
