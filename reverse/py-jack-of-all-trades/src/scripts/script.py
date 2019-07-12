import os
import requests
import json
import schedule
import base64
import time
from pathlib import Path

FLAG_PATH = os.path.realpath('/home/guest/flag.txt')
KEY_PATH = os.path.realpath("/home/guest/key.txt")

FLAG = Path(FLAG_PATH).read_text(encoding="UTF-8").strip()
KEY = Path(KEY_PATH).read_text(encoding="UTF-8").strip()

headers = {
    'Content-Type': 'application/json',
}
url = 'http://127.0.0.1:8080'

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


def send_ciphertext(msg, key):
    ciphertext = encrypt_mod128(msg, key)
    ciphertext_b64 = base64.b64encode(ciphertext.encode(
        encoding="UTF-8")).decode(encoding="UTF-8")
    payload = {
        'ciphertext': ciphertext_b64
    }
    try:
        requests.post(url, headers=headers, data=json.dumps(payload))
    except:
        pass

if __name__ == '__main__':
    schedule.every(3).seconds.do(lambda: send_ciphertext(FLAG, KEY))
    while True:
        schedule.run_pending()
        time.sleep(1)
