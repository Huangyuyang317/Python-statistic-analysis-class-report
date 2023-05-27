# manager.py
import socket
import threading
import os
import time

class Manager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("聊天室服务器启动，等待连接...")

        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        name = client.recv(1024).decode()
        self.broadcast(f"{name} 进入聊天室")
        self.clients[client] = name
        self.send_message(client, "欢迎进入聊天室！")

        while True:
            try:
                message = client.recv(1024).decode()
                if message == "/quit":
                    self.remove_client(client)
                    break
                elif message.startswith("@"):
                    self.send_private_message(client, message)
                else:
                    self.broadcast(f"{name}: {message}")
            except ConnectionResetError:
                self.remove_client(client)
                break

    def broadcast(self, message):
        with self.lock:
            for client in self.clients:
                self.send_message(client, message)

    def send_private_message(self, sender, message):
        recipient_name, message = message.split(" ", 1)
        for client, name in self.clients.items():
            if name == recipient_name and client != sender:
                self.send_message(client, f"(Private) {self.clients[sender]}: {message}")
                self.send_message(sender, f"(Private) To {name}: {message}")
                break
        else:
            self.send_message(sender, f"找不到用户 {recipient_name}")

    def send_message(self, client, message):
        try:
            client.sendall(message.encode())
        except ConnectionResetError:
            self.remove_client(client)

    def remove_client(self, client):
        name = self.clients[client]
        self.broadcast(f"{name} 离开聊天室")
        self.clients.pop(client)
        client.close()
        self.save_chat_log(f"{name} 离开聊天室")

    def save_chat_log(self, message):
        log_file = "chat_log.txt"
        with open(log_file, "a") as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file.write(f"[{timestamp}] {message}\n")

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    chat_manager = Manager(host, port)
    chat_manager.start()
