import io
import socketserver

from Crypto.PublicKey import RSA


class Keys:
    SERVER_PUB_KEY = None
    SERVER_PRIV_KEY = None
    CLIENT_PUB_KEY = None


class PacketHandler(socketserver.StreamRequestHandler):
    def handle(self):
        opcode = int.from_bytes(self.rfile.read(4), byteorder="big")
        payload_length = int.from_bytes(self.rfile.read(4), byteorder="big")
        payload = self.rfile.read(payload_length)

        # HANDSHAKE
        if opcode == 0:
            # print("Received handshake (new client key)")
            # Payload = client public key
            Keys.CLIENT_PUB_KEY = RSA.importKey(payload)

            # Generate a new RSA key for the server
            Keys.SERVER_PRIV_KEY = RSA.generate(bits=1024)
            Keys.SERVER_PUB_KEY = Keys.SERVER_PRIV_KEY.publickey()

            # Send the opcode and the server pubkey
            export_pub_key = Keys.SERVER_PUB_KEY.exportKey()

            buf = io.BytesIO()
            buf.write(opcode.to_bytes(4, byteorder="big"))
            buf.write(len(export_pub_key).to_bytes(4, byteorder="big"))
            buf.write(export_pub_key)

            buf.seek(0)
            self.wfile.write(buf.read())

        # FLAG PARTS
        elif opcode in range(1, 6):
            if Keys.SERVER_PRIV_KEY:
                plaintext = Keys.SERVER_PRIV_KEY.decrypt(payload)
                # print("Received flag part", opcode - 1, plaintext.decode("utf-8"))

                encrypted, = Keys.CLIENT_PUB_KEY.encrypt(plaintext, 32)

                buf = io.BytesIO()
                buf.write(opcode.to_bytes(4, byteorder="big"))
                buf.write(len(encrypted).to_bytes(4, byteorder="big"))
                buf.write(encrypted)

                buf.seek(0)
                self.wfile.write(buf.read())

        self._close()

    def _close(self):
        self.finish()
        self.connection.close()


def start_server():
    server = socketserver.TCPServer(("127.0.0.1", 8080), PacketHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


if __name__ == '__main__':
    start_server()
