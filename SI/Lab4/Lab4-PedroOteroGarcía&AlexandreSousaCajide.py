###################################################################################
#                                                                                 #
# This program creates a user (Server or Client) that allows to send and receive  # 
# messages using the Double Ratchet Protocol.                                     #
#                                                                                 #
# To chat it is need to run the program once as Client and another as server.     # 
# Then the Client can start the chat.                                             #
#                                                                                 #
###################################################################################                                                                                 #
# Authors:  Pedro Otero García & Alexandre Sousa Cajide                           #
###################################################################################
CLIENT = True # This constant is used to run the program as Server or Client.
# CLIENT = False # False => Server.
###################################################################################

import paho.mqtt.client as mqtt
from threading import Thread
# GENERATE_DH, DH
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
# KDF_RK, KDF_CK
from hkdf import hkdf_expand, hkdf_extract
import hashlib
# KDF_CK
import hmac
# ENCRYPT
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding  # - Import to use the padding.
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
# HEADER
from cryptography.hazmat.primitives import serialization

# CONSTANTS
MAX_SKIP = 10
SK = b'\xfbS!2\xdf\x99\xdf3D9\x9f\xddz\x87\xf2\xf6 \xa0\xda\xc1\xef`VC07\xf4\xd6|\x0e\x17\x90'
DH_PRIV_SERVER = b'\xc8\xb6\xca\xf5\xf6\xa8\x84\xf8\x9d\xbe\x93o\xe8A&g|R\x0e\x1b\xec\xbeW$\x8a\x9f\x85\xf9\x82q\x9aT'
DH_PUB_SERVER = b'\x0b\x0ft\x83\xd7b\x89\xa3\xe8s\xfew\xbbYM\xa0\xb7\xb6O<0\xfe\x87\xf4\xe0\xbb\x05\x91\x8f\xbb\x14\x08'
AD_SERVER = b"ASSOCIATED DATA SERVER"
AD_SERVER = hashlib.sha256(AD_SERVER).digest()#32B
AD_CLIENT = b"ASSOCIATED DATA CLIENT"
AD_CLIENT = hashlib.sha256(AD_CLIENT).digest()#32B

# MQTT broker address and port
mqttBroker = '18.101.47.122'
password = 'HkxNtvLB3GC5GQRUWfsA'
mqtt_id = 'sinf'
port = 1883
MQTT_IN = "mike.in" # Where SERVER receives messages.
MQTT_OUT = "mike.out" # Where CLIENT receives messages.

class DH_pair:
    def __init__(self, dh_priv: [bytes]*32, dh_pub: [bytes]*32) -> None:
        self.dh_priv = dh_priv
        self.dh_pub = dh_pub

class HEADER:
    def __init__(self, dh_pair=DH_pair, pn: int = 0, n: int = 0) -> None:
        if dh_pair is not None:
            self.dh = dh_pair.dh_pub
            self.pn = pn
            self.n = n

    def to_bytes(self):
        pn_b = self.pn.to_bytes(1, byteorder='big') # 1B
        n_b = self.n.to_bytes(1, byteorder='big') # 1B

        return self.dh + pn_b + n_b 
    
    def to_object(self, header_bytes: [bytes]*34):
        self.dh = header_bytes[:32]
        self.pn = int.from_bytes(header_bytes[32:33], byteorder='big')
        self.n = int.from_bytes(header_bytes[33:34], byteorder='big')

def CONCAT(ad: [bytes]*32, header: HEADER):
    return ad + header.to_bytes() #66B

def GENERATE_DH():
    # Generate a new DH pair key.
    dh_priv = X25519PrivateKey.generate()
    dh_pub = dh_priv.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
    dh_priv = dh_priv.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())
    
    return DH_pair(dh_priv, dh_pub)

def DH(dh_pair: DH_pair, dh_pub: bytes):
    # Perform DH calculation between private key and public key
    dh_priv_key = X25519PrivateKey.from_private_bytes(data=dh_pair.dh_priv)
    dh_pub_key = X25519PublicKey.from_public_bytes(data=dh_pub)
    return dh_priv_key.exchange(dh_pub_key)

def KDF_RK(rk: bytes, dh_out: bytes) -> [[bytes]*32, [bytes]*32]:
    prk = hkdf_extract(salt=rk, input_key_material=dh_out, hash=hashlib.sha512)
    key = hkdf_expand(pseudo_random_key=prk, info=b"Info KDF_RK", length=64, hash=hashlib.sha512)

    return key[:32],key[32:] # Root Key, Chain Key

def KDF_CK(ck: bytes) -> [[bytes]*32, [bytes]*32]:
    new_ck = hmac.new(key=ck, msg=b'Chain Key', digestmod=hashlib.sha512)
    mk = hmac.new(key=ck, msg=b'Message Key', digestmod=hashlib.sha512)

    return new_ck.digest()[:32], mk.digest()[:32] # Chain Key, Message Key

def ENCRYPT(mk: bytes, plaintext: bytes, assotiate_data: bytes):
    # Key Derivation Function
    output_length = 80
    prk = hkdf_extract(salt=bytes(output_length), input_key_material=mk, hash=hashlib.sha512)
    exp = hkdf_expand(pseudo_random_key=prk, info=b"Info ENCRYPT/DECRYPT", length=output_length, hash=hashlib.sha512)

    sk = exp[:32] # Encryption Key
    ak = exp[32:64] # Authentication Key
    iv = exp[64:] # Initialization vector

    # Construct an AES-128-GCM Cipher object with the generated encryption key and IV.
    encryptor = Cipher(
            algorithms.AES(key=sk),
            modes.GCM(initialization_vector=iv),
            backend=default_backend()
        ).encryptor()

    padder = padding.PKCS7(128).padder()
    padder_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padder_data) + encryptor.finalize()
    tag = encryptor.tag # Tag is always 16B long.

    # HMAC for authentication of the associate it data.
    ad = hmac.new(key=ak, msg=assotiate_data, digestmod=hashlib.sha512).digest() # 512b = 64B

    return tag + ad + ciphertext

def DECRYPT(mk: bytes, ciphertext: bytes, assotiate_data: bytes):
    tag = ciphertext[:16]
    ad_original = ciphertext[16:16+64]
    ciphertext = ciphertext[16+64:]

    # Key Derivation Function
    output_length = 80
    prk = hkdf_extract(salt=bytes(output_length), input_key_material=mk, hash=hashlib.sha512)
    exp = hkdf_expand(pseudo_random_key=prk, info=b"Info ENCRYPT/DECRYPT", length=output_length, hash=hashlib.sha512)

    sk = exp[:32] # Encryption Key
    ak = exp[32:64] # Authentication Key
    iv = exp[64:] # Initialization vector

    decryptor = Cipher(
        algorithms.AES(key=sk),
        modes.GCM(initialization_vector=iv, tag=tag),
        backend=default_backend()
    ).decryptor()

    # Decryption and unpadding.
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(plaintext) + unpadder.finalize()

    # HMAC for authentication of the associate it data.
    ad = hmac.new(key=ak, msg=assotiate_data, digestmod=hashlib.sha512).digest() # 512b = 64B

    if ad != ad_original:
        raise Exception("Error authenticating data.")
    
    return plaintext


class User:
    '''
        This class implements the double ratchet protocol functionalities for a 
        user server and a user client. 
    '''
    def __init__(self) -> None:
        return
    
    def RatchetInitClient(self, SK, server_dh_public_key):
        self.DHs = GENERATE_DH()
        self.DHr = server_dh_public_key
        self.RK, self.CKs = KDF_RK(SK, DH(self.DHs, self.DHr)) 
        self.CKr = None
        self.Ns = 0
        self.Nr = 0
        self.PN = 0
        self.MKSKIPPED = {}

    def RatchetInitServer(self, SK, server_dh_pair):
        self.DHs = server_dh_pair
        self.DHr = None
        self.RK = SK
        self.CKs = None
        self.CKr = None
        self.Ns = 0
        self.Nr = 0
        self.PN = 0
        self.MKSKIPPED = {}

    def RatchetDecrypt(self, header, ciphertext: bytes, AD: bytes):
        plaintext = self.TrySkippedMessageKeys(header, ciphertext, AD)
        if plaintext != None:
            return plaintext
        if header.dh != self.DHr:                 
            self.SkipMessageKeys(header.pn)
            self.DHRatchet(header)
        self.SkipMessageKeys(header.n)             
        self.CKr, mk = KDF_CK(self.CKr)
        self.Nr += 1
        return DECRYPT(mk, ciphertext, CONCAT(AD, header))

    def TrySkippedMessageKeys(self, header: HEADER, ciphertext: bytes, AD: bytes):
        if (header.dh, header.n) in self.MKSKIPPED:
            mk = self.MKSKIPPED[header.dh, header.n]
            del self.MKSKIPPED[header.dh, header.n]
            return DECRYPT(mk, ciphertext, CONCAT(AD, header))
        else:
            return None

    def SkipMessageKeys(self, until):
        if self.Nr + MAX_SKIP < until:
            Exception("SkipMessage exception.")
        if self.CKr != None:
            while self.Nr < until:
                self.CKr, mk = KDF_CK(self.CKr)
                self.MKSKIPPED[self.DHr, self.Nr] = mk
                self.Nr += 1

    def DHRatchet(self, header):
        self.PN = self.Ns                          
        self.Ns = 0
        self.Nr = 0
        self.DHr = header.dh
        self.RK, self.CKr = KDF_RK(self.RK, DH(self.DHs, self.DHr))
        self.DHs = GENERATE_DH()
        self.RK, self.CKs = KDF_RK(self.RK, DH(self.DHs, self.DHr))

    def RatchetEncrypt(self, plaintext, AD):
        self.CKs, mk = KDF_CK(self.CKs)
        header = HEADER(self.DHs, self.PN, self.Ns)
        self.Ns += 1
        return header, ENCRYPT(mk, plaintext, CONCAT(AD, header))

###################################################################################
# This user instance represent the user that will publish and receive messages.
u = User()
###################################################################################

def on_message(client, userdata, message):
    '''
        Function to handle a receiving message.
    '''
    m = message.payload
    header = HEADER(dh_pair=None)
    header.to_object(header_bytes=m[:34])
    c = m[34:]
    if CLIENT:
        ad = AD_SERVER
        name = "[CLIENT][MESSAGE RECEIVED]: "
    else:
        ad = AD_CLIENT
        name = "[SERVER][MESSAGE RECEIVED]:"
    plaintext = u.RatchetDecrypt(header=header,ciphertext=c,AD=ad)
    print(name + plaintext.decode())

def subscriber(topic):
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_id, password=password)
    client.connect(mqttBroker)

    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()

def publisher(name: str, topic: str, ad: [bytes]*32) -> None:
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_id, password=password)
    client.connect(mqttBroker)

    while True:
        m = input("\n" + name + "[SEND A MESSAGE]: ")
        header, c = u.RatchetEncrypt(plaintext=m.encode(), AD=ad)
        c = header.to_bytes() + c # Header: 34B
        client.publish(topic, c)
        print("\nJust published " + str(c) + " to topic "+ topic + ".")

def main():
    '''
        This function creates the user and the threads to publish and read messages.
    '''
    server_dh_pair = DH_pair(dh_priv=DH_PRIV_SERVER, dh_pub=DH_PUB_SERVER)
    
    if CLIENT:
        name = "[CLIENT]"
        u.RatchetInitClient(SK=SK, server_dh_public_key=DH_PUB_SERVER)
        ad = AD_CLIENT
        sub_topic = MQTT_OUT
        pub_topic = MQTT_IN
    else:
        name = "[SERVER]"
        u.RatchetInitServer(SK=SK, server_dh_pair=server_dh_pair)
        ad = AD_SERVER
        sub_topic = MQTT_IN
        pub_topic = MQTT_OUT

    t_publisher = Thread(target=publisher, args=(name, pub_topic, ad,))
    t_subscriber = Thread(target=subscriber, args=(sub_topic,))
    t_publisher.start()
    t_subscriber.start()

main()    
