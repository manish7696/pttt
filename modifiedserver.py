import socket 
import threading
import pyaudio


# Define constants for audio streaming
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_PACKET_SIZE = 4096

audio = pyaudio.PyAudio()
reciever_stream = audio.open(format=FORMAT, rate=RATE, output=True, channels=CHANNELS, frames_per_buffer=CHUNK)
# sender_stream = audio.open(format=FORMAT, rate=RATE, input=True, channels=CHANNELS, frames_per_buffer=CHUNK)

clients = {}
lock = threading.Lock()

def handle_client(client_socket, client_address):
    client_identifier = f"{client_address[0]}:{client_address[1]}"
    clients[client_identifier] = client_socket
    print(f"Accepted connection from {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            data_length = len(data.strip())

            if data_length == 4:
                # Acquire the lock when data with length 4 is received
                lock.acquire()
                try:
                    # Process data with length 4
                    print(f"Received data with length 4 from {client_identifier}: {data.decode('utf-8')}")
                    # Process the data as needed
                finally:
                    # Release the lock after processing
                    lock.release()
            elif data_length == 3:
                # Process data with length 3
                print(f"Received data with length 3 from {client_identifier}: {data.decode('utf-8')}")
                # Process the data as needed

            
    except Exception as e:
        print(f"Error with client {client_identifier}: {e}")

    finally:
        # Clean up and remove the client from the dictionary when they disconnect
        client_socket.close()
        del clients[client_identifier]
        print(f"Connection with {client_identifier} closed")

def connections():
    server_ip = '0.0.0.0'
    server_port = 6000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(3)
    print(f"Server listening on {server_ip}:{server_port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler_thread.start()

if __name__ == "__main__":
    connection_thread = threading.Thread(target=connections)
    connection_thread.start()
