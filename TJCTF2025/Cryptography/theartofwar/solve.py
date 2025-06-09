from Crypto.Util.number import *
from gmpy2 import iroot
n = []
c = []
e = None

with open(r"E:\CTF\TJCTF2025\Cryptography\theartofwar\output.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("e ="):
            e = int(line.split("=")[1].strip())
        elif line.startswith("n"):
            n.append(int(line.split("=")[1].strip()))
        elif line.startswith("c"):
            c.append(int(line.split("=")[1].strip()))

def extended_gcd(a:int,b:int)->int:
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b!= 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0

def modular_inverse(a:int,m:int)->int:
    x,y = extended_gcd(a,m)
    return (x%m)

def CRT(a: list, m:list)->int:
	M = 1
	for i in range(len(a)):
		M = M*m[i]

	p = [M//m[i] for i in range(len(m))]
	p1 = [modular_inverse(p[i],m[i]) for i in range(len(m))]
	result=0
	for i in range(len(a)):
		result = result + p[i]*p1[i]*a[i]
	return result%M 

m_pow_e = CRT(c, n)
m = iroot(m_pow_e, e)[0]
print("Decrypted message:", long_to_bytes(int(m)).decode())