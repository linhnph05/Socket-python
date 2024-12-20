# Socket-python
## Communication Scenario of the Program

### Protocol Exchange between Client and Server

#### Server Startup:
- The server opens a UDP socket and listens on a specific IP address and port.
- The server reads the list of available files from the specified directory and stores this information in a data structure (dictionary).

#### Client Startup:
- The client opens a UDP socket and connects to the server's IP address and port.
- The client sends a "LIST" request to the server to receive the list of available files.

### File List Request (LIST):
- The client sends a "LIST" message to the server.
- The server receives the "LIST" message, reads the list of files from the specified directory, and sends this list back to the client as a text string.

### File Download Request (DOWNLOAD):
- The client reads the file names from the input.txt file and sends a download request to the server.
- The server receives the request, checks for the file's existence, and sends the file size to the client.
- The server sends the file data in chunks and waits for an ACK from the client after each chunk.

### Receive Data and Send ACK:
- The client receives the file data from the server and sends an ACK message to confirm receipt of the data chunk.
- This process continues until the entire file is downloaded.

### Complete File Download:
- When the server sends an "EOF" message, the client knows that the file download is complete.
- The client saves the file to the specified directory and continues to check the input.txt file for new files to download.

## Message Structure

### File List Request Message (LIST):
- **Content:** "LIST"
- **Data Type:** Text string

### File Download Request Message (DOWNLOAD):
- **Content:** "DOWNLOAD <file_name> <offset> <chunk_size>"
- **Data Type:** Text string

### ACK Message:
- **Content:** "ACK"
- **Data Type:** Text string

### EOF Message:
- **Content:** "EOF"
- **Data Type:** Text string

## Data Types of Messages
- All messages are sent as text strings and are encoded before being sent over the socket.

## Database Organization (if any)
- The program does not use a complex database. Instead, it uses a text file (file_list.txt) to store the list of available files on the server.
- Information about the files is stored in a dictionary with the file name as the key and the file size as the value.

## Detailed Description

### Server
- Reads the list of files from the specified directory and stores it in a dictionary.
- Listens for requests from the client.
- Handles the "LIST" request and sends the file list to the client.
- Handles the "DOWNLOAD" request, sends the file size and file data in chunks, and waits for ACK from the client.

### Client
- Sends a "LIST" request to receive the file list from the server and displays the list.
- Reads file names from input.txt and sends a "DOWNLOAD" request to the server.
- Receives file data from the server, sends ACK after each data chunk, and saves the file to the specified directory.
- Continues to check input.txt for new files to download.
# Setup for 1 machine
## Setup for MacOS/Linux
```
git clone https://github.com/linhnph05/Socket-python
cd Socket-python
python3 -m venv venv 
source venv/bin/activate
```

### Client
```
python3 client.py
```

### Server
```
python3 server.py
```

## Setup for Windows

```
git clone https://github.com/linhnph05/Socket-python
cd Socket-python
python3 -m venv venv 
.\venv\Scripts\activate
```

### Client
```
python3 client.py
```

### Server
```
python3 server.py
```

# Setup for 2 machine
## MacOS/Linux
### Client
```
git clone https://github.com/linhnph05/Socket-python
python3 -m venv venv 
source venv/bin/activate

python3 client.py
```
### Server
```
git clone https://github.com/linhnph05/Socket-python
python3 -m venv venv 
source venv/bin/activate

python3 server.py
```

## Windows
### Client
```
git clone https://github.com/linhnph05/Socket-python
cd Socket-python/
python3 -m venv venv 
.\venv\Scripts\activate
python3 client.py
```
### Server
```
git clone https://github.com/linhnph05/Socket-python
cd Socket-python/
python3 -m venv venv 
.\venv\Scripts\activate
python3 server.py
```