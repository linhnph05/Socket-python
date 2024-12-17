import socket
import os

def udp_file_server(host, port, files_directory):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Server listening on {host}:{port}")

    while True:
        file_request, addr = sock.recvfrom(1024)
        file_name = file_request.decode()
        file_path = os.path.join(files_directory, file_name)

        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            sock.sendto(str(file_size).encode(), addr)

            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    sock.sendto(data, addr)
                    ack, _ = sock.recvfrom(1024)
                    if ack.decode() != 'ACK':
                        print(f"Failed to receive ACK from {addr}")
                        break
                    print(f"Sent {len(data)} bytes to {addr}")
            sock.sendto(b'EOF', addr)  # End of file
        else:
            sock.sendto(b'File not found', addr)
            print(f"File {file_name} not found, notified {addr}")

if __name__ == "__main__":
    udp_file_server('0.0.0.0', 12345, 'files_directory')