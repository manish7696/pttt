import socket
from pydub import AudioSegment
from pydub.playback import play
import pyaudio 
import threading
#import RPi.GPIO as GPIO

server_ip = '0.0.0.0'
server_port = 6000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_PACKET_SIZE = 4096
audio = pyaudio.PyAudio()
reciever_stream = audio.open(format=FORMAT, rate = RATE, output=True, channels=CHANNELS, frames_per_buffer = CHUNK)

print(f"Server listening on {server_ip}:{server_port}")

client_address = None

'''
#gpio pin setup
GPIO.setmode(GPIO.BCM)
gpio_pin = 17
GPIO.setup(gpio_pin, GPIO.OUT)
'''

def recieve_audio():
    while True:

        global client_address
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
    
        # Create a file to save the received audio data as a WAV file
        audio_file = AudioSegment.silent(duration=0)  # Initialize an empty AudioSegment
    
        try:
            while True:

                data = client_socket.recv(1024)  # Receive data in chunks
            
                if data == b"high":
                    print("relay on")
                    #GPIO.output(gpio_pin, GPIO.LOW)
                if data == b"low":
                    print("relay off")  
                    #GPIO.output(gpio_pin, GPIO.HIGH)

                if not data:
                    break
                #print(data)
                reciever_stream.write(data)
                # audio_chunk = AudioSegment.from_file(data, format="wav")  # Load audio chunk
                # audio_file += audio_chunk  # Append the received audio chunk
                # play(audio_chunk)  # Play the received audio chunk
        except Exception as e:
            print(f"Error: {e}")
        finally:
            audio_file.export('received_audio.wav', format="wav")  # Export the final audio
            client_socket.close()
            print("Connection closed")

recieving_thread = threading.Thread(target=recieve_audio)
recieving_thread.start()

