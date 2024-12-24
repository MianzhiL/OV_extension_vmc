import socket
import threading

class UDPReceiver:
    """A UDP receiver that listens for incoming data and invokes a callback function.

    Attributes:
        callback (function): The function to call with received data.
        ip (str): The IP address to bind the socket to.
        port (int): The port number to listen on.
        stop_event (threading.Event): Event used to signal the receiving thread to stop.
        sock (socket.socket): The UDP socket used for receiving data.
    """
        
    def __init__(self, callback, ip='127.0.0.1', port=39539):
        """Initialize the UDPReceiver.

        Args:
            callback (function): The function to call with received data.
            ip (str): The IP address to bind the socket to (default is '127.0.0.1').
            port (int): The port number to listen on (default is 39539).
        """
        self.callback = callback
        self.ip = ip
        self.port = port
        self.stop_event = threading.Event()
        self.sock=None

    def start(self):
        self.stop_event.clear()
        threading.Thread(target=self.receive_data, daemon=True).start()

    def stop(self):
        self.stop_event.set()
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass   # Socket may already be closed; ignore exception
            finally:
                self.sock.close() # Close the socket
        print("Socket closed.")

    def receive_data(self):
        """Receive data from the UDP socket and invoke the callback."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

        print(f"Listening on UDP port {self.port}...")
        
        while not self.stop_event.is_set():
            try:
                data, addr = self.sock.recvfrom(65535)  # Receive data
                if data:
                    self.callback(data)
            except OSError as e:
                if self.stop_event.is_set():
                    print("Socket closed, stopping receive loop.")
                    break
                else:
                    raise e
