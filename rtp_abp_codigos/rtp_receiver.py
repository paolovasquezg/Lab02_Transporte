import socket
import struct
import time

def rtp_receiver():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(('127.0.0.1', 5005))

    expected_seq_num = 0

    while True:
        rtp_packet, addr = receiver_socket.recvfrom(1024)
        # extract all from packet
        payload = rtp_packet[12:].decode()
        _, _, seq_num, timestamp, _ = struct.unpack('!BBHII', rtp_packet[:12])

        current_time = int(time.time())
        delay = current_time - timestamp

        if delay > 2:
            print(f"Timestamp: {timestamp}, Current Time: {int(time.time())}")
            print(f"Received packet with Seq: {seq_num} but timestamp is not current, ignoring.")
            continue

        if seq_num == expected_seq_num:
            print(f"Received packet with Seq: {seq_num}, Payload: {payload}")
            ack_packet = struct.pack('!H', seq_num)
            receiver_socket.sendto(ack_packet, addr)
            print(f"Sent ACK for Seq: {seq_num}")
            expected_seq_num = (expected_seq_num + 1) % 2
        else:
            print(f"Out-of-order packet received with Seq: {seq_num}, expected Seq: {expected_seq_num}")
            expected_seq_num = (expected_seq_num + 1) % 2


if __name__ == "__main__":
    rtp_receiver()
