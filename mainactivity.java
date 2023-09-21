import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {
    private Socket socket;
    private OutputStream outputStream;

    private EditText ipAddressEditText;
    private Button connectButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ipAddressEditText = findViewById(R.id.editTextIpAddress);
        connectButton = findViewById(R.id.buttonConnect);

        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                connectToServer();
            }
        });
    }

    private void connectToServer() {
        final String ipAddress = ipAddressEditText.getText().toString();
        final int port = 6000; // Replace with your port number

        // Create a socket and connect to the server on a background thread
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    socket = new Socket();
                    socket.connect(new InetSocketAddress(ipAddress, port));
                    outputStream = socket.getOutputStream();

                    // Connection successful, send a string
                    String messageToSend = "Hello, Server!";
                    outputStream.write(messageToSend.getBytes());
                    outputStream.flush();

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            showMessage("Connected to the server and sent a message!");
                        }
                    });
                } catch (IOException e) {
                    e.printStackTrace();
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            showMessage("Failed to connect to the server.");
                        }
                    });
                }
            }
        }).start();
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

