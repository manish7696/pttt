# import socket
# import pyaudio
# import threading
# import os
# from kivy.lang import Builder
# from kivymd.app import MDApp
# from kivymd.uix.button import MDRaisedButton
# from kivymd.uix.boxlayout import MDBoxLayout


# # Your configuration variables go here (same as in the original code)
# SENDER_HOST = '0.0.0.0'
# SENDER_PORT = 12345
# RECEIVER_IP = '192.168.29.183'
# RECEIVER_PORT = 12346
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 1024
# MAX_PACKET_SIZE = 4096
# server_ip = '192.168.29.183'
# server_port = 12356

# # Initialize PyAudio and create streams (same as in the original code)
# audio = pyaudio.PyAudio()
# sender_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
# receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# # Set up sockets (same as in the original code)
# sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# receiver_socket.bind((SENDER_HOST, RECEIVER_PORT))
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ptt_active = False
# stop_event = threading.Event()

# def send_audio():
#     while not stop_event.is_set():
#         while True:
#             if ptt_active:
#                 data = sender_stream.read(CHUNK)
#                 for i in range(0, len(data), MAX_PACKET_SIZE):
#                     chunk = data[i:i+MAX_PACKET_SIZE]
#                     sender_socket.sendto(chunk, (RECEIVER_IP, RECEIVER_PORT))

# def receive_audio():
#     while not stop_event.is_set():
#         while True:
#             data, _ = receiver_socket.recvfrom(MAX_PACKET_SIZE)
#             receiver_stream.write(data)

# # Start sender and receiver threads (same as in the original code)
# sender_thread = threading.Thread(target=send_audio)
# receiver_thread = threading.Thread(target=receive_audio)
# sender_thread.start()
# receiver_thread.start()

# # KV = '''
# # BoxLayout:
# #     orientation: 'vertical'

# #     MDRaisedButton:
# #         text: "PTT"
# #         on_press: app.ptt_pressed()
# #         on_release: app.ptt_released()
# # '''

# class PTTApp(MDApp):
#     def build(self):
#         layout = MDBoxLayout(orientation='horizontal', spacing=10)
#         pttbutton = MDRaisedButton(text='PTT', on_press=self.ptt_pressed, on_release=self.ptt_released)
#         quitbutton = MDRaisedButton(text='QUIT')

#         layout.add_widget(pttbutton)
#         layout.add_widget(quitbutton)

#         return layout

#     def ptt_pressed(self, event):
#         global ptt_active
#         ptt_active = True
#         print("Talking...")
#         client_socket.sendto(b'high', (server_ip, server_port))

#     def ptt_released(self, event):
#         global ptt_active
#         ptt_active = False
#         print("Not talking...")
#         client_socket.sendto(b'low', (server_ip, server_port))

#     def quit_app(self):
#         stop_event.set()

#         sender_thread.join()
#         receiver_thread.join()

#         sender_socket.close()
#         receiver_socket.close()
#         client_socket.close()

#         sender_stream.stop_stream()
#         sender_stream.close()
#         receiver_stream.stop_stream()
#         receiver_stream.close()

#         audio.terminate()
#         os._quit()

# if __name__ == '__main__':
#     PTTApp().run()

import socket
import pyaudio
import threading
import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.config import Config
from kivy.core.window import Window


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


audio = pyaudio.PyAudio()
sender_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
receiver_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind((SENDER_HOST, RECEIVER_PORT))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ptt_active = False

# def send_audio():
#     print('sending audio')
#     while True:
#         if ptt_active:
#             data = sender_stream.read(CHUNK)
#             for i in range(0, len(data), MAX_PACKET_SIZE):
#                 chunk = data[i:i+MAX_PACKET_SIZE]
#                 sender_socket.sendto(chunk, (RECEIVER_IP, RECEIVER_PORT))
#         else:
#             break

def receive_audio():
    while True:
        data, _ = receiver_socket.recvfrom(MAX_PACKET_SIZE)
        receiver_stream.write(data)


# sender_thread = threading.Thread(target=send_audio_loop)
receiver_thread = threading.Thread(target=receive_audio, daemon=True)
receiver_thread.start()


class PTTApp(MDApp):
    
    def build(self):
        Window.size = (300, 100)
        layout = MDBoxLayout(orientation='horizontal', spacing=10)
        pttbutton = MDRaisedButton(text='PTT', on_press=self.ptt_pressed, on_release=self.ptt_released)
        quitbutton = MDRaisedButton(text='QUIT', on_press = self.quit_app)

        layout.add_widget(pttbutton)
        layout.add_widget(quitbutton)

        return layout

    # def ptt_pressed(self, ev):
    #     global ptt_active
    #     ptt_active = True
    #     while ptt_active:
    #         send_audio()
    #         print("Talking...")
        # client_socket.sendto(b'high', (server_ip, server_port))

    def ptt_pressed(self, ev):
        global ptt_active
        ptt_active = True
        print("Talking...")
        self.start_send_audio()

    def send_audio_loop(self):
        while True:
            if ptt_active:
                data = sender_stream.read(CHUNK)
                for i in range(0, len(data), MAX_PACKET_SIZE):
                    chunk = data[i:i + MAX_PACKET_SIZE]
                    sender_socket.sendto(chunk, (RECEIVER_IP, RECEIVER_PORT))
            else:
                break

    def start_send_audio(self):
        audio_thread = threading.Thread(target=self.send_audio_loop, daemon=True)
        audio_thread.start()


    def ptt_released(self, ev):
        global ptt_active
        ptt_active = False
        print("ptt false\nNot talking...")
        # client_socket.sendto(b'low', (server_ip, server_port))

    def quit_app(self, ev):
        os._exit(0)

if __name__ == '__main__':
    PTTApp().run()