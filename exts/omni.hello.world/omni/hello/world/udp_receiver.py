import socket
import threading

class UDPReceiver:
    def __init__(self, callback, ip='127.0.0.1', port=39539):
        self.callback = callback
        self.ip = ip
        self.port = port
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.receive_data).start()

    def stop(self):
        self.running = False

    def receive_data(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip, self.port))

        print(f"Listening on UDP port {self.port}...")
        
        while self.running:
            data, addr = sock.recvfrom(4096)  # 接收数据
            if data:
                self.callback(data)
