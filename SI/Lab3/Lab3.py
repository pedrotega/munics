import os

import secrets
import numpy as np

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding  # - Import to use the padding.
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)


AES_LENGTH = 128
NUM_NODES = 13
NODES = list(range(1, NUM_NODES + 1))
INPUT_FILE = "intro20.mp4"
OUTPUT_FILE = "new.mp4"
NODE_SELECTED = 12 # Node selected to decrypt the message.
T = [10,8,13] # Nodes that were compromised.


def generate_aes_key() -> bytes:
    # Generate a random 128-bit (16-byte) key
    aes_key = secrets.token_bytes(16)
    return aes_key


def generate_aes_keys() -> list:
    # Generate a key for each node.
    aes_keys = []
    for _ in range(NUM_NODES):
        aes_keys.append(generate_aes_key())

    return aes_keys


def encryptAESBlock(key: bytes, plaintext: bytes) -> bytes:
    # Generate a random 128-bit IV.
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padder_data = padder.update(plaintext) + padder.finalize()

    # Construct an AES-128-CBC Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend(),
    ).encryptor()

    # Encrypt the plaintext and get the associated ciphertext.
    #ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    ciphertext = encryptor.update(padder_data) + encryptor.finalize()

    return (iv, ciphertext)


def decryptAESBlock(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    # Construct a Cipher object, with the key, iv
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    ).decryptor()

    # Decryption gets us the plaintext.
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(plaintext) + unpadder.finalize()

    return plaintext


def read_file(name: str) -> bytes:
    in_file = open(name, "rb") # opening for [r]eading as [b]inary
    data = in_file.read() 
    in_file.close()

    return data


def write_file(bts: bytes, name: str) -> None:
    with open(name, "wb") as binary_file:
        binary_file.write(bts)


def computePath2Root(n: int) -> list:
    path = [n]
    u = n
    while path[-1] != 1:
        father = int(np.floor(u/2))
        path.append(father)
        u = father

    return path


def computeS(T: list) -> list:
    # Compute the cover S for set T.
    S = []
    if len(T) == 0:
        # If any node were compromised the cover is the root.
        return [1]
    
    compromised = []
    for i in T:
        path = computePath2Root(i)
        compromised += path

    candidates = [x for x in NODES if x not in compromised]
    for j in candidates:
        if j % 2 == 0:
            sibling = j + 1
        else:
            sibling = j - 1

        if sibling in compromised:
            S.append(j)

    return S


def AACS(m: bytes, T: list, aes_keys: list) -> (list, list):
    # 1 - Generate a random key k.
    k = generate_aes_key()
    # 2 - Computing cover S.
    S = computeS(T)
    # 3 - Computing c_us.
    iv = []
    c = []
    for u in S:
        iv_u, c_u = encryptAESBlock(aes_keys[u-1], k)
        c.append(c_u)
        iv.append(iv_u)
    # 4 - Encrypting the message with the generated key. 
    iv_m, c_m =  encryptAESBlock(k, m)
    iv.append(iv_m)
    c.append(c_m)

    return iv, c


def main():

    if NODE_SELECTED not in NODES:
        print("The node \"",NODE_SELECTED,"\" is unreachable.")
        return

    m = read_file(INPUT_FILE)
    aes_keys = generate_aes_keys()
    iv, c = AACS(m, T, aes_keys)

    S = computeS(T)
    node_i = NODE_SELECTED
    while(True):
        if node_i in S:
            for pos, node in enumerate(S):
                if node_i == node:
                    original_key = decryptAESBlock(aes_keys[node_i-1], iv[pos], c[pos])
                    message = decryptAESBlock(original_key, iv[-1], c[-1])
                    write_file(message, OUTPUT_FILE)
                    print("Message decrypted successfully.")
                    print("\t> Key used:", node_i)
                    return
        
        # If node_i is the root and is not in the cover it 
        # means that NODE_SELECTED was compromised.
        if node_i == 1:
            print("The node \"",NODE_SELECTED,"\" has been compromised, information cannot be obtained.")
            return
        
        # If node_i is not in the cover there are two scenarios:
        #   1 - node_i was compromised.
        #   2 - One of its ascents is in the cover.
        father = int(np.floor(node_i/2))
        node_i = father
    

main()

