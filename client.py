import socket
import os
import time

def request_file_list(sock, server_address):
    sock.sendto("LIST".encode(), server_address)
    response, _ = sock.recvfrom(4096)
    response = response.decode()
    print("Available files on server:")
    print(response)

def udp_file_client(server_host, server_port, input_file, output_directory):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (server_host, server_port)
    downloaded_files = set()

    # Request and display the list of files on the server
    request_file_list(sock, server_address)

    while True:
        with open(input_file, 'r') as file_list:
            for file_name in file_list:
                file_name = file_name.strip()
                if not file_name or file_name in downloaded_files:
                    continue

                sock.sendto(file_name.encode(), server_address)
                print(f"Requested file: {file_name}")

                output_file_path = os.path.join(output_directory, file_name)
                with open(output_file_path, 'wb') as f:
                    total_received = 0
                    file_size = None
                    progress_threshold = 0.25  # 25%
                    next_progress = progress_threshold
                    idx = 1
                    while True:
                        data, _ = sock.recvfrom(4096)
                        if data == b'File not found':
                            print(f"File {file_name} not found on server")
                            break
                        if data == b'EOF':
                            print(f"File transfer for {file_name} completed")
                            break

                        if file_size is None:
                            file_size = int(data.decode())
                            continue

                        f.write(data)
                        total_received += len(data)
                        sock.sendto(b'ACK', server_address)

                        if file_size:
                            percent_downloaded = total_received / file_size
                            if percent_downloaded >= next_progress:
                                print(f"Downloading {file_name} part {idx} ... {int(next_progress * 100)}%")
                                next_progress += progress_threshold
                                idx += 1

                downloaded_files.add(file_name)

        time.sleep(5)

if __name__ == "__main__":
    udp_file_client('127.0.0.1', 12345, 'input.txt', 'download_directory')