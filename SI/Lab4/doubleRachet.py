# GENERATE_DH, DH
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
# KDF_RK, KDF_CK
from hkdf import hkdf_expand, hkdf_extract
import hashlib
# KDF_CK
import hmac
# ENCRYPT
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding  # - Import to use the padding.
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
# HEADER
from cryptography.hazmat.primitives import serialization

# CONSTANTS
MAX_SKIP = 10

class DH_pair:
    def __init__(self, dh_priv, dh_pub) -> None:
        self.dh_priv = dh_priv
        self.dh_pub = dh_pub

class HEADER:
    def __init__(self, dh_pair=None, pn: int = 0, n: int = 0) -> None:
        if dh_pair is not None:
            self.dh = dh_pair.dh_pub
            self.pn = pn
            self.n = n

    def to_bytes(self):
        dh_pub_b = self.dh.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw) # 32 B
        pn_b = self.pn.to_bytes(1, byteorder='big') # 1 B
        n_b = self.n.to_bytes(1, byteorder='big') # 1 B

        return dh_pub_b + pn_b + n_b 
    
    def to_object(self, header_bytes: [bytes]*34):
        self.dh = X25519PublicKey.from_public_bytes(data=header_bytes[:32])
        self.pn = int.from_bytes(header_bytes[32:33], byteorder='big')
        self.n = int.from_bytes(header_bytes[33:34], byteorder='big')


def GENERATE_DH():
    # Generate a new DH pair key.
    dh_priv = X25519PrivateKey.generate()
    dh_pub = dh_priv.public_key()
    
    return DH_pair(dh_priv, dh_pub)

def DH(dh_pair, dh_pub):
    # Perform DH calculation between private key and public key
    return dh_pair.dh_priv.exchange(dh_pub)

def KDF_RK(rk: bytes, dh_out: bytes) -> [[bytes]*32, [bytes]*32]:
    prk = hkdf_extract(salt=rk, input_key_material=dh_out, hash=hashlib.sha512)
    key = hkdf_expand(pseudo_random_key=prk, info=b"Info KDF_RK", length=64, hash=hashlib.sha512)

    return key[:32],key[32:] # Root Key, Chain Key

def KDF_CK(ck: bytes) -> [[bytes]*32, [bytes]*32]:
    new_ck = hmac.new(key=ck, msg=b'Chain Key', digestmod=hashlib.sha512)
    mk = hmac.new(key=ck, msg=b'Message Key', digestmod=hashlib.sha512)

    return new_ck.digest()[:32], mk.digest()[:32] # Chain Key, Message Key

# def HEADER(dh_pair, pn: int, n: int):   
#     dh_pub_b = dh_pair.dh_pub.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
#     pn_b = pn.to_bytes(1, byteorder='big')
#     n_b = n.to_bytes(1, byteorder='big')

#     return dh_pub_b + pn_b + n_b

def ENCRYPT(mk: bytes, plaintext: bytes, assotiate_data: bytes):
    # Key Derivation Function
    output_length = 80
    prk = hkdf_extract(salt=bytes(output_length), input_key_material=mk, hash=hashlib.sha512)
    exp = hkdf_expand(pseudo_random_key=prk, info=b"Info ENCRYPT", length=output_length, hash=hashlib.sha512)

    ek = exp[:32] # Encryption Key
    ak = exp[32:64] # Authentication Key
    iv = exp[64:] # Initialization vector

    # Construct an AES-128-GCM Cipher object with the generated encryption key and IV.
    encryptor = Cipher(
            algorithms.AES(key=ek),
            modes.GCM(initialization_vector=iv),
            backend=default_backend()
        ).encryptor()

    padder = padding.PKCS7(128).padder()
    padder_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padder_data) + encryptor.finalize()
    tag = encryptor.tag # Tag is always 16B long.

    # HMAC for authentication of the associate it data.
    ad = hmac.new(key=ak, msg=assotiate_data, digestmod=hashlib.sha512).digest() # 512b = 64B
    print(len(ad))
    
    return tag + ad + ciphertext

def CONCAT(ad: bytes, header: HEADER):
    

    return ad + header

def RatchetDecrypt(self, header, ciphertext, AD):
    plaintext = TrySkippedMessageKeys(self, header, ciphertext, AD)
    if plaintext != None:
        return plaintext
    if header.dh != self.DHr:                 
        SkipMessageKeys(self, header.pn)
        DHRatchet(self, header)
    SkipMessageKeys(self, header.n)             
    self.CKr, mk = KDF_CK(self.CKr)
    self.Nr += 1
    return DECRYPT(mk, ciphertext, CONCAT(AD, header))

def TrySkippedMessageKeys(self, header, ciphertext, AD):
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

def RatchetInitAlice(self, SK, bob_dh_public_key):
    self.DHs = GENERATE_DH()
    self.DHr = bob_dh_public_key
    self.RK, self.CKs = KDF_RK(SK, DH(self.DHs, self.DHr)) 
    self.CKr = None
    self.Ns = 0
    self.Nr = 0
    self.PN = 0
    self.MKSKIPPED = {}

def RatchetInitBob(self, SK, bob_dh_key_pair):
    self.DHs = bob_dh_key_pair
    self.DHr = None
    self.RK = SK
    self.CKs = None
    self.CKr = None
    self.Ns = 0
    self.Nr = 0
    self.PN = 0
    self.MKSKIPPED = {}