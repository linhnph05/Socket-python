import socket
import threading
import time
import os
from tqdm import tqdm
import pyfiglet
import sys

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
            # print(file_info)
            download_file(file_name, file_info[file_name]) 
            processed_files.add(file_name)
        
        time.sleep(5)  


def download_chunk(file_name, part, offset, chunk_size, output_folder):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(f"DOWNLOAD {file_name} {offset} {chunk_size}".encode())

    part_path = os.path.join(output_folder, f"{file_name}.part{part}")
    with open(part_path, "wb") as f, tqdm(
        total=chunk_size,
        unit='B',
        unit_scale=True,
        desc=f"Part {part}",
        dynamic_ncols=True,
        position=part,  # Position ensures each bar is rendered on a separate line
        leave=True     # Leave the progress bar after completion
    ) as progress_bar:
        received = 0
        while received < chunk_size:
            data = client.recv(min(chunk_size - received, 1024))  # Read up to remaining size or 4KB
            if not data:
                break
            f.write(data)
            received += len(data)
            progress_bar.update(len(data))  # Always update by the length of received data
        # Force synchronization of progress to ensure 100% display
        progress_bar.n = chunk_size
        progress_bar.last_print_n = chunk_size
        progress_bar.refresh()
    if received == chunk_size:
        tqdm.write(f"Part {part} downloaded successfully")
    else:
        tqdm.write(f"Warning: Incomplete chunk for part {part}. Expected {chunk_size}, got {received} bytes.")
    
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
    last_chunk_size = file_size - (chunk_size * (num_parts - 1))

    threads = []
    for i in range(num_parts):
        offset = i * chunk_size
        size = last_chunk_size if i == num_parts - 1 else chunk_size
        thread = threading.Thread(target=download_chunk, args=(file_name, i, offset, size, output_folder))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    merge_chunks(file_name, output_folder, num_parts)
    # print(f"Download complete: {file_name}")

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
    # print(file_info)

    client.close()

def display_banner(text):
    banner = pyfiglet.figlet_format(text)
    print(banner)

def client_program():
    input_file = "input.txt" 
    display_banner("CLIENT")
    request_file_list()
    monitor_thread = threading.Thread(target=monitor_input_file, args=(input_file,))
    monitor_thread.daemon = True  # Cho phép dừng luồng khi chương trình chính kết thúc
    monitor_thread.start()

    while True:
        a = 1


if __name__ == "__main__":
    client_program()
