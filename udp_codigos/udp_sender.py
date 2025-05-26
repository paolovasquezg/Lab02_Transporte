import socket
import zlib
import struct

# Función para generar el checksum
def checksum_calculator(data):
    checksum = zlib.crc32(data)
    return checksum

UDP_IP = "192.168.233.172"
UDP_PORT = 5005
MESSAGE = b"Si lo lees, nos debe un punto extra en el lab1"

print("IP destino UDP: %s" % UDP_IP)
print("Puerto destino UDP: %s" % UDP_PORT)
print("mensaje: %s" % MESSAGE)

data_length = len(MESSAGE)
print("Longitud del dato: %s" % data_length)

# checksum = checksum_calculator(MESSAGE)
checksum = int("4", 16)  # valor de checksum forzado
print("Checksum: %s" % checksum)

# Construcción del encabezado
udp_header = struct.pack("!IIII", UDP_PORT, UDP_PORT, data_length, checksum)
print("Encabezado: %s" % udp_header)

MESSAGE = udp_header + MESSAGE  # concatenación

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
