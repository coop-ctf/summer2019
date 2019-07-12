import io
import math
import socket
import textwrap
import time
from pathlib import Path

from Crypto.PublicKey import RSA

FLAG = Path('/home/guest/flag.txt').read_text().strip()

FLAG_PARTS = textwrap.wrap(FLAG, int(math.ceil(len(FLAG)) / 5))


class Keys:
    SERVER_PUB_KEY = None
    CLIENT_PUB_KEY = None
    CLIENT_PRIV_KEY = None


def perform_client():
    clientsocket = new_socket()
    send_and_receive_handshake(clientsocket)
    clientsocket.close()
    time.sleep(0.5)

    for i in range(len(FLAG_PARTS)):
        clientsocket = new_socket()
        send_and_receive_part(clientsocket, i)
        clientsocket.close()
        time.sleep(0.5)


def send_and_receive_handshake(clientsocket: socket.socket):
    Keys.CLIENT_PRIV_KEY = RSA.generate(bits=1024)
    Keys.CLIENT_PUB_KEY = Keys.CLIENT_PRIV_KEY.publickey()

    pub_key_payload = Keys.CLIENT_PUB_KEY.exportKey()
    buf = io.BytesIO()
    buf.write(int(0).to_bytes(4, byteorder="big"))
    buf.write(len(pub_key_payload).to_bytes(4, byteorder="big"))
    buf.write(pub_key_payload)

    buf.seek(0)
    clientsocket.sendall(buf.read())

    buf = io.BytesIO()
    clientsocket.settimeout(5)
    while True:
        data = clientsocket.recv(1024)
        if not data:
            break
        buf.write(data)

    buf.seek(0)
    opcode = int.from_bytes(buf.read(4), byteorder="big")
    if opcode != 0:
        # print("invalid opcode", opcode, "expected", 0)
        return

    payload_length = int.from_bytes(buf.read(4), byteorder="big")
    payload = buf.read(payload_length)
    Keys.SERVER_PUB_KEY = RSA.importKey(payload)


def send_and_receive_part(clientsocket: socket.socket, index: int):
    part = FLAG_PARTS[index]
    encrypted, = Keys.SERVER_PUB_KEY.encrypt(part.encode("utf-8"), 32)

    buf = io.BytesIO()
    buf.write(int(index + 1).to_bytes(4, byteorder="big"))
    buf.write(len(encrypted).to_bytes(4, byteorder="big"))
    buf.write(encrypted)

    buf.seek(0)
    clientsocket.sendall(buf.read())

    buf = io.BytesIO()
    clientsocket.settimeout(5)
    while True:
        data = clientsocket.recv(1024)
        if not data:
            break
        buf.write(data)

    buf.seek(0)
    opcode = int.from_bytes(buf.read(4), byteorder="big")
    if opcode != index + 1:
        # print("invalid opcode", opcode, "expected", index + 1)
        raise Exception()

    payload_length = int.from_bytes(buf.read(4), byteorder="big")
    payload = buf.read(payload_length)
    decrypted = Keys.CLIENT_PRIV_KEY.decrypt(payload)
    if decrypted.decode("utf-8") != part:
        # print(decrypted.decode("utf-8"), "did not match part", index, part)
        raise Exception()


def new_socket() -> socket.socket:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('127.0.0.1', 8080))
    return clientsocket


def run():
    while True:
        try:
            perform_client()
        except Exception as e:
            # print(e)
            pass
        time.sleep(5)


if __name__ == '__main__':
    run()
