import socket
import struct
import time
import random

# Crea el paquete RTP con encabezado y payload
def create_rtp_packet(seq_num, payload):
    version = 2
    padding = 0
    extension = 0
    csrc_count = 0
    marker = 0
    payload_type = 96
    ssrc = 1234
    # Empaqueta el encabezado RTP: Version, PT, Seq, Timestamp, SSRC
    rtp_header = struct.pack('!BBHII',
                             (version << 6) | (padding << 5) | (extension << 4) | csrc_count,
                             payload_type,
                             seq_num,
                             int(time.time()),
                             ssrc)
    return rtp_header + payload.encode()

# Función principal del emisor
def rtp_sender():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_address = ('127.0.0.1', 5005)
    sender_socket.settimeout(2)  # timeout de retransmisión

    seq_num = 0
    payloads = ["Mensaje 1", "Mensaje 2", "Mensaje 3"]

    for payload in payloads:
        while True:
            rtp_packet = create_rtp_packet(seq_num, payload)

            if random.random() < 0.3:
                print(f"[Simulated] Sent packet with Seq: {seq_num} loss.")
                seq_num = (seq_num + 1) % 2
                continue
            elif random.random() > 0.3 and random.random() < 0.5:
                delay = 5
                print(f"[Simulated] Sent packet with Seq: {seq_num} delay.")
                time.sleep(delay)

            sender_socket.sendto(rtp_packet, receiver_address)
            print(f"Sent packet with Seq: {seq_num}, Payload: {payload}")

            try:
                ack_packet, _ = sender_socket.recvfrom(1024)
                ack_seq_num = struct.unpack('!H', ack_packet[:2])[0]

                if ack_seq_num == seq_num:
                    print(f"Received ACK for Seq: {seq_num}")
                    seq_num = (seq_num + 1) % 2
                    break
                else:
                    print(f"Duplicate ACK received for Seq: {ack_seq_num}, waiting retransmisión...")
            except socket.timeout:
                print(f"Timeout! Resending packet with Seq: {seq_num}")
                # seq_num = (seq_num + 1) % 2
                # print("Timeout!")

            time.sleep(2)


if __name__ == "__main__":
    rtp_sender()
