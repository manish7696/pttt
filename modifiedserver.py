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

def handle_client(client_socket, client_address):
    client_identifier = f"{client_address[0]}:{client_address[1]}"
    clients[client_identifier] = client_socket
    print(f"Accepted connection from {client_address}")

    try:
        while True:
            # Receive and process data from the client here
            data = client_socket.recv(1024)
            print(data)
            # if not data:
            #     break
            # # Process data as needed
            
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

