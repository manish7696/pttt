import socket
import pyaudio
import threading
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.core.window import Window
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)

SENDER_HOST = '0.0.0.0'
SENDER_PORT = 4096
RECEIVER_IP = '192.168.53.219'
RECEIVER_PORT = 12346
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_PACKET_SIZE = 4096
server_ip = '192.168.29.183'
server_port = 12356

audio = pyaudio.PyAudio()
sender_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((SENDER_HOST, RECEIVER_PORT))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ptt_active = False

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 70  # Add some padding to center the button vertically

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        MDRaisedButton:
            text: "PTT"
            on_press: app.ptt_pressed()
            on_release: app.ptt_released()
            size_hint: None, None
            size: 200, 50
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
'''

class PTTApp(MDApp):
    sender_thread = None

    def build(self):
        Window.size = (360, 600)
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def ptt_pressed(self):
        global ptt_active
        ptt_active = True
        print("Talking...")
        self.sender_thread = threading.Thread(target=self.send_audio)
        self.sender_thread.start()

    def ptt_released(self):
        global ptt_active
        ptt_active = False
        if self.sender_thread:
            self.sender_thread.join()  # Wait for the sender_thread to finish
        print("Not talking...")
        client_socket.sendto(b'low', (server_ip, server_port))

    def quit_app(self):
        logging.info("Key Pressed")
        try:
            self.stop()
        except Exception as e:
            print('error here: ', e)

    def send_audio(self):
        while ptt_active:
            data = sender_stream.read(CHUNK)
            for i in range(0, len(data), MAX_PACKET_SIZE):
                chunk = data[i:i+MAX_PACKET_SIZE]
                sender_socket.sendto(chunk, (RECEIVER_IP, RECEIVER_PORT))

    def receive_audio(self):
        while True:
            data, _ = receiver_socket.recvfrom(MAX_PACKET_SIZE)
            receiver_stream.write(data)

if __name__ == '__main__':
    app = PTTApp()
    receiver_thread = threading.Thread(target=app.receive_audio)
    receiver_thread.daemon = True  # Set the receiving thread as a daemon so it runs continuously in the background
    receiver_thread.start()
    app.run()

