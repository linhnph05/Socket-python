import socket
import os

def load_file_list(files_directory):
    file_list = {}
    for file_name in os.listdir(files_directory):
        file_path = os.path.join(files_directory, file_name)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            file_list[file_name] = file_size
    return file_list

def udp_file_server(host, port, files_directory):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Server listening on {host}:{port}")

    while True:
        file_request, addr = sock.recvfrom(1024)
        request = file_request.decode()

        if request == "LIST":
            file_list = load_file_list(files_directory)
            response = "\n".join([f"{file_name} {size}B" for file_name, size in file_list.items()])
            sock.sendto(response.encode(), addr)
            continue

        file_name = request
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