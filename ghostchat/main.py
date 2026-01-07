import socket
import threading
import curses
import sys

from config import HOST, PORT
from network.socket_manager import SocketManager
from network.protocol import encode_message, decode_message
from ui.chat_ui import ChatUI
from storage.logger import log_message, prune_logs

username = input("Username: ")
ui = ChatUI(username)
running = True


def receive_loop(sock_mgr):
    global running
    while running:
        data = sock_mgr.receive()
        if not data:
            ui.add_message("SYSTEM", "Connection closed.")
            running = False
            break

        msg = decode_message(data)

        if msg["type"] == "quit":
            ui.add_message("SYSTEM", f"{msg['sender']} left the chat.")
            running = False
            break

        ui.add_message(msg["sender"], msg["message"])
        log_message(msg["sender"], msg["message"], msg["timestamp"])
        prune_logs()


def start_chat(sock_mgr):
    def send_callback(text):
        nonlocal sock_mgr
        if text.strip().lower() == "/quit":
            sock_mgr.send(encode_message("quit", username))
            ui.running = False
            return

        sock_mgr.send(encode_message("chat", username, text))
        ui.add_message(username, text)

    curses.wrapper(ui.run, send_callback)


def start_server():
    print(f"[SYSTEM] Listening on port {PORT}")  # fallback output

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    conn, addr = server.accept()
    ui.add_message("SYSTEM", f"Connected from {addr}")

    sock_mgr = SocketManager(conn)

    threading.Thread(target=receive_loop, args=(sock_mgr,), daemon=True).start()
    start_chat(sock_mgr)


def start_client(target_ip):
    print("[SYSTEM] Connecting to server...")  # fallback output

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, PORT))

    ui.add_message("SYSTEM", "Connected to server.")
    sock_mgr = SocketManager(sock)

    threading.Thread(target=receive_loop, args=(sock_mgr,), daemon=True).start()
    start_chat(sock_mgr)


if __name__ == "__main__":
    mode = input("server / client? ").strip().lower()

    if mode == "server":
        start_server()
    else:
        ip = input("Target IP: ")
        start_client(ip)

    sys.exit(0)
