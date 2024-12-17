import socket
import threading

class UDPReceiver:
    def __init__(self, callback, ip='127.0.0.1', port=39539):
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
                pass  # 套接字可能已经被关闭，无需处理异常
            finally:
                self.sock.close() # Close the socket
        print("Socket closed.")

    def receive_data(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

        print(f"Listening on UDP port {self.port}...")
        
        while not self.stop_event.is_set():
            try:
                data, addr = self.sock.recvfrom(65535)  # 接收数据
                if data:
                    self.callback(data)
            except OSError as e:
                if self.stop_event.is_set():
                    print("Socket closed, stopping receive loop.")
                    break
                else:
                    raise e
