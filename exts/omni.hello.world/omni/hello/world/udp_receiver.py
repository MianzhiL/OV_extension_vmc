import socket
import threading

class UDPReceiver:
    def __init__(self, callback, ip='127.0.0.1', port=39539):
        self.callback = callback
        self.ip = ip
        self.port = port
        self.running = False
        self.sock=None

    def start(self):
        self.running = True
        threading.Thread(target=self.receive_data).start()

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.shutdown(socket.SHUT_RDWR)  # Shut down both read and write
            self.sock.close()  # Close the socket
        print("Socket closed.")

    def receive_data(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

        print(f"Listening on UDP port {self.port}...")
        
        while self.running:
            data, addr = self.sock.recvfrom(65535)  # 接收数据
            if data:
                self.callback(data)
