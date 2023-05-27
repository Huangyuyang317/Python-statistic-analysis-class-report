# chatter.py
import socket
import threading
import os
import time

class Chatter:
    def __init__(self):
        self.host = ""
        self.port = 5000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = ""
        self.exit_flag = threading.Event()
        self.lock = threading.Lock()

    def start(self):
        self.host = input("请输入聊天室的主机IP地址: ")
        self.sock.connect((self.host, self.port))
        self.name = input("请输入您的名字: ")
        self.sock.sendall(self.name.encode())
        threading.Thread(target=self.receive_messages).start()
        threading.Thread(target=self.send_messages).start()

    def receive_messages(self):
        while not self.exit_flag.is_set():
            try:
                message = self.sock.recv(1024).decode()
                print(message)
            except ConnectionResetError:
                print("与服务器的连接已断开。")
                break

    def send_messages(self):
        while not self.exit_flag.is_set():
            message = input()
            if message == "/quit":
                self.exit_flag.set()
                self.sock.sendall(message.encode())
                break
            self.sock.sendall(message.encode())

    def save_chat_log(self, message):
        log_file = "chat_log.txt"
        with open(log_file, "a") as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file.write(f"[{timestamp}] {message}\n")

if __name__ == "__main__":
    chatter = Chatter()
    chatter.start()
