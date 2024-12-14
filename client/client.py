import socket
import threading
import time
import os

HOST = '127.0.0.1'
PORT = 12345
CHUNK_SIZE = 1024 * 1024  # 1 MB

file_info = {}  # Dictionary để lưu thông tin file

def read_input_file(input_file, processed_files):
    try:
        with open(input_file, "r") as f:
            lines = f.read().splitlines()
        new_files = [file for file in lines if file not in processed_files]
        return new_files
    except FileNotFoundError:
        print(f"File {input_file} not found. Please create it.")
        return []

def monitor_input_file(input_file):
    processed_files = set()  # Lưu các file đã xử lý
    while True:
        new_files = read_input_file(input_file, processed_files)
        
        # Xử lý từng file mới
        for file_name in new_files:
            print(f"New file detected: {file_name}")
            print(file_info)
            download_file(file_name, file_info[file_name]) 
            processed_files.add(file_name)
        
        time.sleep(5)  


def download_chunk(file_name, part, offset, chunk_size, output_folder):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(f"DOWNLOAD {file_name} {offset} {chunk_size}".encode())
    data = client.recv(chunk_size)

    part_path = os.path.join(output_folder, f"{file_name}.part{part}")
    with open(part_path, "wb") as f:
        f.write(data)

    client.close()


def merge_chunks(file_name, output_folder, num_parts):
    with open(file_name, "wb") as output_file:
        for part in range(num_parts):
            part_path = os.path.join(output_folder, f"{file_name}.part{part}")
            with open(part_path, "rb") as f:
                output_file.write(f.read())
            os.remove(part_path)


def download_file(file_name, file_size):
    output_folder = "./downloads"
    os.makedirs(output_folder, exist_ok=True)
    num_parts = 4
    chunk_size = file_size // num_parts

    threads = []
    for i in range(num_parts):
        offset = i * chunk_size
        thread = threading.Thread(target=download_chunk, args=(file_name, i, offset, chunk_size, output_folder))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    merge_chunks(file_name, output_folder, num_parts)
    print(f"Download complete: {file_name}")

def request_file_list():
    global file_info # Reset dictionary
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall("LIST".encode())
    response = client.recv(4096).decode()
    print("Available files:")
    print(response)

    
    file_info.clear()
    for line in response.splitlines():
        name, size = line.split()
        file_info[name] = int(size)  # Lưu tên file và kích thước vào dictionary
    print(file_info)

    client.close()

def client_program():
    input_file = "input.txt" 

    request_file_list()
    monitor_thread = threading.Thread(target=monitor_input_file, args=(input_file,))
    monitor_thread.daemon = True  # Cho phép dừng luồng khi chương trình chính kết thúc
    monitor_thread.start()

    while True:
        a = 1


if __name__ == "__main__":
    client_program()
