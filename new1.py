import socket
import pyaudio
import threading
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

# Your configuration variables go here (same as in the original code)
SENDER_HOST = '0.0.0.0'
SENDER_PORT = 12345
RECEIVER_IP = '192.168.29.183'
RECEIVER_PORT = 12346
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_PACKET_SIZE = 4096
server_ip = '192.168.29.183'
server_port = 12356

# Initialize PyAudio and create streams (same as in the original code)
audio = pyaudio.PyAudio()
sender_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Set up sockets (same as in the original code)
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((SENDER_HOST, RECEIVER_PORT))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ptt_active = False

def send_audio():
    while True:
        if ptt_active:
            data = sender_stream.read(CHUNK)
            for i in range(0, len(data), MAX_PACKET_SIZE):
                chunk = data[i:i+MAX_PACKET_SIZE]
                sender_socket.sendto(chunk, (RECEIVER_IP, RECEIVER_PORT))

def receive_audio():
    while True:
        data, _ = receiver_socket.recvfrom(MAX_PACKET_SIZE)
        receiver_stream.write(data)

# Start sender and receiver threads (same as in the original code)
sender_thread = threading.Thread(target=send_audio)
receiver_thread = threading.Thread(target=receive_audio)
sender_thread.start()
receiver_thread.start()

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDRaisedButton:
        text: "PTT"
        on_press: app.ptt_pressed()
        on_release: app.ptt_released()
'''

class PTTApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def ptt_pressed(self):
        global ptt_active
        ptt_active = True
        print("Talking...")
        client_socket.sendto(b'high', (server_ip, server_port))

    def ptt_released(self):
        global ptt_active
        ptt_active = False
        print("Not talking...")
        client_socket.sendto(b'low', (server_ip, server_port))

if __name__ == '__main__':
    PTTApp().run()
import socket
import pyaudio
import threading
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

# Your configuration variables go here (same as in the original code)
SENDER_HOST = '0.0.0.0'
SENDER_PORT = 12345
RECEIVER_IP = '192.168.29.183'
RECEIVER_PORT = 12346
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_PACKET_SIZE = 4096
server_ip = '192.168.29.183'
server_port = 12356

# Initialize PyAudio and create streams (same as in the original code)
audio = pyaudio.PyAudio()
sender_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Set up sockets (same as in the original code)
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((SENDER_HOST, RECEIVER_PORT))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ptt_active = False

def send_audio():
    while True:
        if ptt_active:
            data = sender_stream.read(CHUNK)
            for i in range(0, len(data), MAX_PACKET_SIZE):
                chunk = data[i:i+MAX_PACKET_SIZE]
                sender_socket.sendto(chunk, (RECEIVER_IP, RECEIVER_PORT))

def receive_audio():
    while True:
        data, _ = receiver_socket.recvfrom(MAX_PACKET_SIZE)
        receiver_stream.write(data)

# Start sender and receiver threads (same as in the original code)
sender_thread = threading.Thread(target=send_audio)
receiver_thread = threading.Thread(target=receive_audio)
sender_thread.start()
receiver_thread.start()

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDRaisedButton:
        text: "PTT"
        on_press: app.ptt_pressed()
        on_release: app.ptt_released()
'''

class PTTApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def ptt_pressed(self):
        global ptt_active
        ptt_active = True
        print("Talking...")
        client_socket.sendto(b'high', (server_ip, server_port))

    def ptt_released(self):
        global ptt_active
        ptt_active = False
        print("Not talking...")
        client_socket.sendto(b'low', (server_ip, server_port))

if __name__ == '__main__':
    PTTApp().run()
