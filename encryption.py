import random
import hashlib
import string
from binascii import hexlify
from math import lcm, gcd

# ok this is fast
class RSA:
    def rabinMiller(self, num):
        """Rabin-Miller primality test."""
        s = num - 1
        t = 0

        while s % 2 == 0:
            s = s // 2
            t += 1
        for trials in range(5):
            a = random.randrange(2, num - 1)
            v = pow(a, s, num)
            if v != 1:
                i = 0
                while v != (num - 1):
                    if i == t - 1:
                        return False
                    else:
                        i = i + 1
                        v = (v ** 2) % num
            return True

    def is_prime(self, num):
        """Checks if a number is a Primenumber using the Rabin-Miller primality test."""
        lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                    67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
                    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
                    251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
                    353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449,
                    457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569,
                    571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661,
                    673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
                    797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
                    911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

        if num in lowPrimes:
            return True
        for prime in lowPrimes:
            if num % prime == 0:
                return False
        return self.rabinMiller(num)

    def get_primes(self, bits=1024):
        """Gets two random prime numbers with the specifies bit length."""
        while True:
            p = random.getrandbits(bits)
            if self.is_prime(p):
                break
            else:
                continue

        while True:
            q = random.getrandbits(bits)
            if self.is_prime(q):
                break
            else:
                continue

        return p, q

    def generate_rsa_keys(self, e=65537, bits=1024):
        """Generates public and private keys for RSA."""
        p, q = self.get_primes(bits=bits)
        n = p * q
        lambda_n = lcm(p - 1, q - 1)
        d = pow(e, -1, lambda_n)

        public_key = (n, e)
        private_key = (lambda_n, d)

        return public_key, private_key

    def byte_xor(self, ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    def sxor(self, s1, s2):
        return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

    def i2osp(self, integer: int, size: int = 4) -> str:
        return b"".join([chr((integer >> (8 * i)) & 0xFF).encode() for i in reversed(range(size))])

    def mgf1(self, input_str: bytes, length: int, hash_func=hashlib.sha256) -> str:
        """Mask generation function."""
        counter = 0
        output = b""
        while len(output) <= length:
            C = self.i2osp(counter, 4)
            output += hash_func(input_str + C).digest()
            counter += 1
        return output[:length]

    def get_bit_len(self, msg: str):
        """Returns length of string in bits."""
        return len(msg.encode('utf-8'))*8

    def generate_padding(self, message: str, n: int, k0=128):  # Change k0 and k1 to more secure standards
        # I spent a whole day on this and it still doesnt work
        #message = hexlify(message)
        n = self.get_bit_len(str(n))
        print(n - k0, (n - k0)//8)
        mLen = self.get_bit_len(message)//8
        k = n//8
        k1 = k - 2 * k0 - mLen - 2
        padding_size = '0' * k1

        r = bin(random.randint(0, 2**k0))

        #print(r)

        r_masked = bin(int(hexlify(self.mgf1(r.encode('ascii'), (n - k0)//8)).decode(), 16))
        r_masked = r_masked[2:]
        print('R_masked: ', r_masked)
        print('r: ', r)

        #print(type(r_masked), r_masked)

        #while self.get_bit_len(message) <= n - k0:

        message += padding_size

        # Makes sure that the message is smaller than the maximum encryption size of the algorithm used.
        #if self.get_bit_len(message) >= n - k0:
        #    message = message.removesuffix(padding_size)

        #print(self.get_bit_len(message)//8)
        msg = [bin(ord(x))[2:] for x in message]
        msg = ''.join([x for x in msg])
        message = msg
        #print(type(msg), msg)

        #message = bin(message)

        X = ''.join([str(ord(a) ^ ord(b)) for a,b in zip(message,r_masked)])#message ^ r_masked#self.byte_xor(message.encode('utf-8'), r_masked)
        #print(X)
        X_masked = bin(int(hexlify(self.mgf1(X.encode('ascii'), k0)), 16))
        X_masked = X_masked[2:]
        Y = ''.join([str(ord(a) ^ ord(b)) for a,b in zip(r_masked, X_masked)])
        #print('Y len: ', len(Y))

        return X_masked , Y

    def encrypt_rsa(self, message: str, public_key: tuple):
        """Encrypts a Message using the RSA algorithm."""
        message = [ord(c) for c in message]
        message = [c for c in message]

        cipher_message = []
        for c in message:
            cipher_message.append(pow(c, public_key[1], public_key[0]))

        return cipher_message

    def decrypt_rsa(self, cipher_message: list, public_key: tuple, private_key: tuple):
        """Decrypts a Ciphered Message using the RSA algorithm."""
        enc_msg = []
        for c in cipher_message:
            enc_msg.append(pow(c, private_key[1], public_key[0]))

        return ''.join([chr(c) for c in enc_msg])
