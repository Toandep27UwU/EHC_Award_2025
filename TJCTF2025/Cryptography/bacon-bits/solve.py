baconian = {
'a': '00000',   'b': '00001',
'c': '00010',   'd': '00011',
'e': '00100',   'f': '00101',
'g': '00110',   'h': '00111',
'i': '01000',    'j': '01000',
'k': '01001',    'l': '01010',
'm': '01011',    'n': '01100',
'o': '01101',    'p': '01110',
'q': '01111',    'r': '10000',
's': '10001',    't': '10010',
'u': '10011',    'v': '10011',
'w': '10100',   'x': '10101',
'y': '10110',   'z': '10111'}

#out = "BaV8hcBaTg\`XG[8eXJTfT7h7hCBa4g<`Xg[8EXjTFTWHW8Ba6XHCbATG\`Xg;8eXj4fT7h78bAV8HcBa4G\@XG[XeXJ4fTWHWXBa68hCbA4g<`8G[8e8JTFT7hWXbA6XhcBaTG"
#pre_out = [ord(i) for i in out]
#pre_out = [i+13 for i in pre_out]
#pre_out = [chr(i) for i in pre_out]
#pre_out = ''.join(pre_out)
#print(pre_out)

f = open('E:/CTF/TJCTF2025/Cryptography/bacon-bits/out.txt', 'r')
out = f.read().strip()
pre_out = ''.join([chr(ord(i) + 13) for i in out])
print(pre_out)

ciphertext = "OncEupOnatimeThEreWasaDuDuPOnAtImethERewaSadUdEOnCeUPoNaTimetHErewAsaDuDEoNcEUpOnATiMeThereWAsadUdeOnCEuPoNAtImEThErEWaSaDudeoNCeupOnaT"
new = []

for i in ciphertext:
    if i.isupper():
        new.append(1)
    else:
        new.append(0)

def group_bits_to_ints(bits):
    grouped = []
    for i in range(0, len(bits), 5):
        group = bits[i:i+5]
        value = "".join(map(str, group)) 
        grouped.append(value)
    return grouped

sos = group_bits_to_ints(new)

baconian_rev = {v: k for k, v in baconian.items()}

for i in range(len(sos)):
    sos[i] = baconian_rev[sos[i]]

sos = ''.join(sos)
print(sos)