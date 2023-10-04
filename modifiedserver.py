import socket 
import threading

def connections():
    while True:
        server_ip = '0.0.0.0'
        server_port = 6000

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(3)
        print(f"Server listening on {server_ip}:{server_port}")
        
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

connection_thread = threading.Thread(target=connections)
connection_thread.start()