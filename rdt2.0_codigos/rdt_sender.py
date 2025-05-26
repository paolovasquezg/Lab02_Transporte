import socket
import time
import random
import hashlib

HOST = "0.0.0.0"
PORT = 9006
TIMEOUT = 2


class Sender:
    def __init__(self, host, port):
        self.seq = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (host, port)

    def is_corrupted(self):
        return random.random() < 0.5

    def corrupt_data(self, data):
        if len(data) == 0:
            return data
        index = random.randint(0, len(data) - 1)
        corrupted_char = chr((ord(data[index]) + 1) % 128)
        return data[:index] + corrupted_char + data[index + 1:]

    def compute_checksum(self, data):
        return hashlib.md5(data.encode()).hexdigest()

    def send(self, messages):
        for msg in messages:
            ack_received = False
            while not ack_received:
                checksum = self.compute_checksum(msg)
                payload = msg

                if self.is_corrupted():
                    payload = self.corrupt_data(payload)
                    print(f"[Sender] *** Corrupting packet payload: {payload} ***")

                packet = f"{self.seq}:{checksum}:{payload}"
                print(f"[Sender] Sending packet {self.seq}: {payload}")
                self.sock.sendto(packet.encode(), self.addr)
                self.sock.settimeout(TIMEOUT)

                try:
                    response, _ = self.sock.recvfrom(1024)
                    response = response.decode()
                    print(f"[Sender] Got response: {response}")
                    if response == "ACK":
                        ack_received = True
                        self.seq += 1
                    else:
                        print("[Sender] NAK received. Resending...")
                except socket.timeout:
                    print("[Sender] Timeout. Resending...")
def run_sender():
    time.sleep(1)
    sender = Sender(HOST, PORT)
    sender.send(["Hello", "World", "This", "Is", "RDT 2.0"])

run_sender()
