from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse, GCD
from Crypto.PublicKey import RSA as PYRSA
from sympy import nextprime
from random import randint
#from secret import FLAG
from binascii import unhexlify


class RSA():

    def __init__(self, size):
        self.e = 65537
        phi = 0

        while GCD(self.e, phi) != 1:
            p, q = self.getPrime(size), self.getPrime(size)
            phi = (p - 1) * (q - 1)
            self.n = p * q

        self.d = inverse(self.e, phi)
        self.key = PYRSA.construct((self.n, self.e), True)

    def getPrime(self, size):
        lower = 2**(size - 1) + 2**500
        upper = 2**(size - 1) + 2**501
        n = randint(lower, upper)
        return nextprime(n)

    def encrypt(self, message):
        message = bytes_to_long(message)
        return pow(message, self.e, self.n)

    def decrypt(self, encrypted_message):
        message = pow(encrypted_message, self.d, self.n)
        return long_to_bytes(message)

    def export_key(self):
        return self.key.export_key('PEM').decode()


def main():
    rsa = RSA(1024)
    key = rsa.export_key()
    msg = b"hola"
    enc = long_to_bytes(rsa.encrypt(msg))

    with open("key2.pem", "w") as f:
        f.write(key)

    with open("flag2.enc", "wb") as f:
        f.write(enc)

    f = bytes_to_long(enc)
    #k = bytes_to_long(key)
    plain = rsa.decrypt(f)
    print(plain)

    with open("key.pem", mode="rb") as file:
        key = file.read()

    with open("flag.enc", mode="rb") as file:
        flag = file.read()

    f = bytes_to_long(flag)
    k = bytes_to_long(key)
    plain = rsa.decrypt(f)
    print(plain)
    print(b"\x07\xc2\xa0\x1a".decode())
    b = b"\x07\xc2\xa0\x1a\xbf\x13\xb9\x04\x1c\xe5\x86\xe1\xc5\xa3\xdf\x07\xdd\xf3\xc2\xfc\xb1\xf4\xca\x8b\xb3\x9b\xf8\xae\xe5\xaa\xf2\x8b\x83\x97\xcd\xb2\xcf\x84\x9a\xca\xa8\xaa\xcf\xcb\xe9\xa5\xd6\xde\x9d\x9d\xc9\x04\xae\xdd\xf5\x1f\xd0\xd1\xb2\xc9\xe4\xa3\x13\xdc\xd9\x0e\xac\x8b\xb0\xe9\x02\xd2\xca\xb4\x9b\xf9\x9a\xc1\xd7\xf5\x91\x1f\xee\xfd\x00\x8d\xff\xc3\xdc\x84\x93\xa7\x12\x02\xd8\xab\xb3\x0b\x84\x10\xd1\x87\x94\x8f\x0c\x18\xc5\x10\x93\xc0\x80\xc3\x08\x8f\x82\x84\x8e\x8c\xd0\xcd\x0f\xf4\xde\x0b\xd5\xa9\xe2\x97\x81\x97\xb9\xcc\x88\x1d\x8c\xdf\xc0\x9f\x1a\xa5\x11\x8f\xe4\x81\xf8\x89\xce\x87\xac\xfb\x1f\x8a\x7f\x04\xba\x96\xcf\x11\xb0"
    print(b.decode())
    b = b"\x07\x9f\xc2\xa0\x1a\xa7\xf8\xbf\x13\xb9\x04\x1c\xe5\x86\xe1\xc5\xa3\xdf\x07\xdd\xf3\xc2\xfc\xb1\xf4\xca\x8b\xb3\x9b\xf8\xae\xe5\xaa\xf2\x8b\x83\x97\xcd\xb2\xcf\x84\x9a\xca\xa8\xaa\xcf\xcb\xe9\xa5\xd6\xde\x9d\x9d\xc9\x04\xae\xdd\xf5\x1f\xd0\xd1\xb2\xc9\xe4\xa3\x13\xdc\xd9\x0e\xac\x8b\xb0\xe9\x02\xd2\xca\xb4\x9b\xf9\x9a\xc1\xd7\xf5\x91\x1f\xee\xfd\x00\x8d\xff\xc3\xdc\x84\x93\xa7\x12\x02\xd8\xab\xb3\x0b\x84\x10\xd1\x87\x94\x8f\x0c\x18\xc5\x10\x93\xc0\x80\xc3\x08\x8f\x82\x84\x8e\x8c\xd0\xcd\x0f\xf4\xde\x0b\xd5\xa9\xe2\x97\x81\x97\xb9\xcc\x88\x1d\x8c\xdf\xc0\x9f\x1a\xa5\x11\x8f\xe4\x81\xf8\x89\xce\x87\xac\xfb\x1f\x8a\x7f\x04\xba\x96\xcf\x11\xb0"

if __name__ == "__main__":
    main()
