import os
import socket
import threading

FILE_LIST = {
    "File1.zip": 5 * 1024 * 1024,
    "File2.zip": 10 * 1024 * 1024,
    "File3.zip": 20 * 1024 * 1024,
}

HOST = '127.0.0.1'
PORT = 12345


def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            command = request.split()
            if command[0] == "LIST":
                response = "\n".join([f"{file_name} {size}" for file_name, size in FILE_LIST.items()])
                client_socket.sendall(response.encode())

            elif command[0] == "DOWNLOAD":
                file_name, offset, chunk_size = command[1], int(command[2]), int(command[3])
                print(file_name, offset, chunk_size)
                if file_name not in FILE_LIST:
                    client_socket.sendall(f"ERROR File not found: {file_name}".encode())
                    print("File name not in file list")
                    continue

                file_path = "./files/" + file_name
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        f.seek(offset)
                        # data = f.read(chunk_size)
                        # print(f"{file_name}: Sending {len(data)} bytes from offset {offset} with chunk size {chunk_size}")
                        # client_socket.sendall(data)
                        sent = 0
                        while sent < chunk_size:
                            data = f.read(min(chunk_size - sent, 1024))  # Ensure full chunk is read and sent
                            if not data:
                                break
                            client_socket.sendall(data)
                            sent += len(data)
                        print(f"{file_name}: Sending {sent} bytes from offset {offset} with chunk size {chunk_size}")
                else:
                    client_socket.sendall(f"ERROR File not found on server".encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started at {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
