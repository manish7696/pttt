import socket
import pyaudio
import threading
import os
import time
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window

SENDER_HOST = '0.0.0.0'
SENDER_PORT = 12345
RECEIVER_IP = '192.168.29.183'
RECEIVER_PORT = 12346
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
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
send_audio_thread = None  # Store the send audio thread

class PTTApp(MDApp):
    
    def build(self):
        Window.size = (320, 640)
        layout = MDBoxLayout(orientation='horizontal', spacing=10)
        pttbutton = MDRaisedButton(text='PTT', on_press=self.ptt_pressed, on_release=self.ptt_released)
        quitbutton = MDRaisedButton(text='QUIT', on_press=self.quit_app)

        layout.add_widget(pttbutton)
        layout.add_widget(quitbutton)

        return layout

    def ptt_pressed(self, ev):
        global ptt_active
        ptt_active = True
        print("Talking...")
        self.start_send_audio()  # Start the send audio thread

    def ptt_released(self, ev):
        global ptt_active
        ptt_active = False
        print("ptt false\nNot talking...")

    def send_audio_loop(self):
        while ptt_active:
            try:
                print('sending')
                data = sender_stream.read(CHUNK)
                for i in range(0, len(data), MAX_PACKET_SIZE):
                    chunk = data[i:i + MAX_PACKET_SIZE]
                    sender_socket.sendto(chunk, (RECEIVER_IP, RECEIVER_PORT))
                time.sleep(0.01)  # Add a small delay to control sending rate
            except:
                print('audio processed too fast')

    def start_send_audio(self):
        global send_audio_thread
        if send_audio_thread is None or not send_audio_thread.is_alive():
            send_audio_thread = threading.Thread(target=self.send_audio_loop, daemon=True)
            send_audio_thread.start()

    def quit_app(self, ev):
        os._exit(0)

if __name__ == '__main__':
    PTTApp().run()
