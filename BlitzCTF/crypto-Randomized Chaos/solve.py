import math
from collections import Counter

def rol8(x, n):                          
    n &= 7
    return ((x << n) | (x >> (8 - n))) & 0xFF

MAP = [[0]*256 for _ in range(256)]      
for f in range(256):
    for k in range(256):
        r = rol8(f & (~k & 0xFF), k & 7)
        MAP[f][r] += 1                   

def load_samples(path="output_4.txt"):
    samples = []
    with open(path, "r") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                samples.append(bytes.fromhex(ln))
    return samples

def recover_flag(samples):
    L = len(samples[0])                  
    freq = [Counter() for _ in range(L)]
    for s in samples:
        for i, b in enumerate(s):
            freq[i][b] += 1

    flag = bytearray(L)
    for i in range(L):
        best_f, best_ll = None, -1e100
        for f in range(256):
            if any(MAP[f][r] == 0 for r in freq[i]):
                continue
            ll = 0.0
            for r, c in freq[i].items():     
                ll += c * math.log(MAP[f][r] / 256)
            if ll > best_ll:
                best_ll, best_f = ll, f
        if best_f is None:
            raise RuntimeError(f"Not seen bytes located in {i}")
        flag[i] = best_f
    return flag.decode("ascii")

def main():
    samples = load_samples("output_4.txt")
    print(recover_flag(samples))

if __name__ == "__main__":
    main()
