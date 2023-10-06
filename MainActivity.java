package com.example.rtl;


import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.AudioTrack;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.util.LogPrinter;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import android.util.Log;

public class MainActivity extends AppCompatActivity {

    MediaRecorder mediaRecorder = new MediaRecorder();

    private AudioTrack audioTrack;

    private Socket socket;
    private OutputStream outputStream;

//    private Socket socketforsignals;
//
//    private Socket outputstreamforSignals;
    private static final int RECORD_AUDIO_PERMISSION_CODE = 1;
    private static final int INTERNET_PERMISSION_CODE = 1;

    private EditText ipAddressEditText; // EditText for IP address
    private Button audioStreamButton; // Button for audio streaming
    private ProgressBar progressBar; // Progress bar for connection

    private boolean isSending = false;


    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        // Initialize the EditText for IP address
        ipAddressEditText = findViewById(R.id.editTextIpAddress);

        // Initialize the TextView for messages
        // TextView for messages
        TextView messageTextView = findViewById(R.id.textViewMessage);

        // Initialize the Button for audio streaming
        audioStreamButton = findViewById(R.id.buttonAudioStream);
        audioStreamButton.setEnabled(false); // Initially disabled

        // Initialize the Progress bar for connection
        progressBar = findViewById(R.id.progressBar);
        progressBar.setVisibility(View.GONE);

        // Check and request necessary permissions
        checkAndRequestPermissions();

        Button closeConnectionButton = findViewById(R.id.buttonCloseConnection);
        closeConnectionButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                closeSocketConnection();
            }
        });


        // Set up touch listener to stop audio streaming
        audioStreamButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    isSending = true;
                    try {
                        sendHighSignal();
                    sendTextMessage("Sound");
                    } catch (IOException e) {
//                        throw new RuntimeException(e);
                    }
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    isSending = false;
                    sendLowSignal();
                    stopAudioStreaming();
                    startDataReceiving();
                }
                return false;
            }
        });
    }

    private void checkAndRequestPermissions() {
        String[] permissions = {
                Manifest.permission.RECORD_AUDIO,
                Manifest.permission.INTERNET
        };

        boolean allPermissionsGranted = true;

        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                allPermissionsGranted = false;
                break;
            }
        }

        if (allPermissionsGranted) {
            showMessage("Permissions granted!");
        } else {
            ActivityCompat.requestPermissions(this, permissions, RECORD_AUDIO_PERMISSION_CODE);
            ActivityCompat.requestPermissions(this, permissions, INTERNET_PERMISSION_CODE);

        }
    }

    private void startAudioStreaming() {
        // Check if the socket is null or not connected
        if (socket == null || !socket.isConnected()) {
            showMessage("Socket not connected.");
            return;
        }

//        // Send the text to the server
//        try {
//            outputStream = socket.getOutputStream();
//            outputStream.write("2".getBytes());
            showMessage("number 2");
//
//        } catch (IOException e) {
//            e.printStackTrace();
//            showMessage("Failed to send text.");
//            return;
//        }
    }

    private void stopAudioStreaming() {
//        showMessage("Audio streaming stopped.");
    }

    // Connect to the server with the provided IP address
    public void connectToServer(View view) {
        final String ipAddress = ipAddressEditText.getText().toString();
        final int port = 6000; // Replace with your port number
//        final int portforsignals = 6001;

        progressBar.setVisibility(View.VISIBLE); // Show progress bar

        // Create a socket and connect to the server on a background thread
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    socket = new Socket();
//                    socketforsignals = new Socket();
                    socket.connect(new InetSocketAddress(ipAddress, port));
                    outputStream = socket.getOutputStream();

//                    socketforsignals = new Socket();
//                    socketforsignals.connect(new InetSocketAddress(ipAddress, portforsignals));
//                    outputstreamforSignals = socketforsignals.getOutputStream();
//                    outputStream = socket.getOutputStream();
//                    outputStream.write("Text".getBytes());

                    // Connection successful, enable audio streaming
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            progressBar.setVisibility(View.GONE);
                            showMessage("Connected to the server!");
                            audioStreamButton.setEnabled(true); // Enable audio streaming button
                        }
                    });
                } catch (IOException e) {
                    e.printStackTrace();
                    // Connection failed, show a toast message on the UI thread
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            progressBar.setVisibility(View.GONE);
                            showMessage("Failed to connect to the server.");
                        }
                    });
                }
            }
        }).start();
    }

    private void closeSocketConnection() {
        if (socket != null && socket.isConnected()) {
            try {
                socket.close();
                showMessage("Socket connection closed.");
            } catch (IOException e) {
                e.printStackTrace();
                showMessage("Error closing socket connection: " + e.toString());
            }
        } else {
            showMessage("Socket not connected.");
        }
    }


    //this method is actually used to send audio to the python server
    private void sendTextMessage(final String message) throws IOException {
        if (socket == null || !socket.isConnected()) {
            showMessage("Socket not connected.");
            return;
        }

        int sampleRate = 44100;
        int audioSource = MediaRecorder.AudioSource.MIC;
        int channelConfig = AudioFormat.CHANNEL_IN_MONO;
        int audioFormat = AudioFormat.ENCODING_PCM_16BIT;
        int bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        AudioRecord audioRecord = new AudioRecord(audioSource, sampleRate, channelConfig, audioFormat, bufferSize);

        audioRecord.startRecording();

        byte[] audioBuffer = new byte[bufferSize];

        // Send the text message to the server in a background thread
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    byte[] messageBytes = message.getBytes(StandardCharsets.UTF_8);
                    outputStream = socket.getOutputStream();

                    while (isSending) {
                        int bytesRead = audioRecord.read(audioBuffer, 0, bufferSize);
                        if (bytesRead > 0) {
                            boolean isZeroData = true;
                            for (int i =0; i<bytesRead; i++){
                                if (audioBuffer[i] != 0){
                                    isZeroData = false;
                                    break;
                                }
                            }
                            if (!isZeroData) {
                                // Send audio data
                                outputStream.write(audioBuffer, 0, bytesRead);
                            }
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                    showMessage(e.toString());
                } finally {
                    audioRecord.stop();
                    audioRecord.release();
                }
            }
        }).start();
    }

    //sending signals for controlling relay
    private void sendHighSignal() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    if (socket != null && socket.isConnected()) {
                        OutputStream outputStream = socket.getOutputStream();
                        outputStream.flush();
                        outputStream.write("high\n".getBytes(StandardCharsets.UTF_8));
                        outputStream.flush(); // Flush to send immediately
                        showMessage("High signal sent.");
                    } else {
                        showMessage("Socket not connected.");
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                    showMessage("Error sending high signal: " + e.toString());
                }
            }
        }).start();
    }

    private void sendLowSignal() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    if (socket != null && socket.isConnected()) {
                        OutputStream outputStream = socket.getOutputStream();
                        outputStream.flush();
                        outputStream.write("low\n".getBytes(StandardCharsets.UTF_8));
                        outputStream.flush(); // Flush to send immediately
                        showMessage("Low signal sent.");
                    } else {
                        showMessage("Socket not connected.");
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                    showMessage("Error sending low signal: " + e.toString());
                }
            }
        }).start();
    }

    //thread to receive audio and playing the audio from python server
    private void startDataReceiving() {
        // Check if the socket is null or not connected
        if (socket == null || !socket.isConnected()) {
            showMessage("Socket not connected.");
            return;
        }

        int sampleRate = 44100;
        int channelConfig = AudioFormat.CHANNEL_OUT_MONO;
        int audioFormat = AudioFormat.ENCODING_PCM_16BIT;
        int bufferSize = AudioTrack.getMinBufferSize(sampleRate, channelConfig, audioFormat);
        audioTrack = new AudioTrack(
                AudioManager.STREAM_MUSIC,
                sampleRate,
                channelConfig,
                audioFormat,
                bufferSize,
                AudioTrack.MODE_STREAM
        );
        audioTrack.play();

        // Create a new thread for receiving data
        Thread receiveThread = new Thread(() -> {
            try {
                // Set up input stream to receive data
                InputStream inputStream = socket.getInputStream();
                byte[] buffer = new byte[1024];
//                int showonce = 0;
                while (!isSending) {
                    int bytesRead = inputStream.read(buffer);
                    if (bytesRead > 0) {
//                        if (showonce==0) {
////                            showMessage("received".toString());
//
//                        }
                        StringBuilder hexString = new StringBuilder();
                        for (int i = 0; i < bytesRead; i++) {
                            hexString.append(String.format("%02X ", buffer[i]));
                        }
                        String receivedData = new String(buffer, StandardCharsets.UTF_8);
                        // Log the received hexadecimal data
                        Log.d("ReceivedData", receivedData);
                        audioTrack.write(buffer, 0, bytesRead);

                    }
                }  } catch (IOException e) {
                e.printStackTrace();
                showMessage("Error receiving data: " + e.toString());
            }
        });

        receiveThread.start();
    }


        @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == RECORD_AUDIO_PERMISSION_CODE) {
            boolean allPermissionsGranted = true;
            for (int grantResult : grantResults) {
                if (grantResult != PackageManager.PERMISSION_GRANTED) {
                    allPermissionsGranted = false;
                    break;
                }
            }
            if (allPermissionsGranted) {
                showMessage("Permissions granted!");
            } else {
                showMessage("Permissions denied. The app requires these permissions to work.");
            }
        }
    }

    private void showMessage(final String message) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
            }
        });
    }
}
