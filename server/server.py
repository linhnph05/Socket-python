import os
import socket
import threading
import pyfiglet

FILE_LIST = {
    
}

HOST = '127.0.0.1'
PORT = 12345


def handle_client(client_socket):
    try:
        while True:
            with open("file_list.txt", "r") as file:
                file_lines = file.readlines()
            for line in file_lines:
                file_name, size = line.strip().removesuffix("B").rsplit(maxsplit=1)
                FILE_LIST[file_name] = size
            # print(FILE_LIST)
            request = client_socket.recv(1024).decode()
            if not request:
                break

            command = request.split()
            if command[0] == "LIST":
                response = "\n".join([f"{file_name} {size}B" for file_name, size in FILE_LIST.items()])
                client_socket.sendall(response.encode())

            elif command[0] == "DOWNLOAD":
                file_name, offset, chunk_size = command[1], int(command[2]), int(command[3])
                if file_name not in FILE_LIST:
                    client_socket.sendall(f"ERROR File not found: {file_name}".encode())
                    print("File name not in file list")
                    continue

                file_path = "./files/" + file_name
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        f.seek(offset)
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

def display_banner(text):
    banner = pyfiglet.figlet_format(text)
    print(banner)
    
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    display_banner("SERVER")
    print(f"Server started at {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
