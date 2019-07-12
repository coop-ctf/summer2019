import base64
import json
import os
import threading
from pathlib import Path

import falcon
import waitress

FLAG_PATH = os.environ.get("FLAG_PATH", "/home/guest/flag.txt")
KEY_PATH = os.environ.get("KEY_PATH", "/home/guest/key.txt")

FLAG = Path(FLAG_PATH).read_text(encoding="UTF-8").strip()
KEY = Path(KEY_PATH).read_text(encoding="UTF-8").strip()


def convert_to_ascii_dec(text):
    return [ord(char) for char in text]


def convert_from_ascii_dec(ascii_dec):
    return "".join([chr(code) for code in ascii_dec])


def sub(a, b):
    return [i - j for i, j in zip(a, b)]


def add(a, b):
    return [i + j for i, j in zip(a, b)]


def mod128(a_list):
    return [item % 128 for item in a_list]


def decrypt_mod128(ciphertext, key):
    if len(ciphertext) != len(key):
        return None

    cipher_in_ascii = convert_to_ascii_dec(ciphertext)
    key_in_ascii = convert_to_ascii_dec(key)

    msg_in_ascii = mod128(sub(cipher_in_ascii, key_in_ascii))
    return convert_from_ascii_dec(msg_in_ascii)


def encrypt_mod128(msg, key):
    if len(key) != len(msg):
        return None

    msg_in_ascii = convert_to_ascii_dec(msg)
    key_in_ascii = convert_to_ascii_dec(key)

    ascii_sum = add(msg_in_ascii, key_in_ascii)
    return convert_from_ascii_dec(mod128(ascii_sum))


class CheckRoute:
    def on_post(self, req, resp):
        raw_json = req.bounded_stream.read()

        try:
            parsed = json.loads(raw_json, encoding='UTF-8')
            ciphertext = base64.b64decode(parsed["ciphertext"].encode(
                encoding="UTF-8")).decode(encoding="UTF-8")
            if decrypt_mod128(ciphertext, KEY) == FLAG:
                resp.media = {
                    "success": True
                }
                return
        except Exception:
            pass

        resp.media = {
            "success": False
        }


def run_server():
    api = falcon.API()
    api.add_route("/", CheckRoute())
    waitress.serve(api, host="127.0.0.1", port=8080)


if __name__ == '__main__':
    ciphertext = encrypt_mod128(FLAG, KEY)
    ciphertext_b64 = base64.b64encode(ciphertext.encode(
        encoding="UTF-8")).decode(encoding="UTF-8")
    threading.Thread(target=run_server).start()
