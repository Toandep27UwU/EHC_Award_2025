# Free Candy [crypto] - Writeup 

## Tóm tắt đề
Challenge có một RNG được định nghĩa bởi đại số quaternion trên prime p. Service tạo **2 bản sao RNG** với cùng tham số q:

1. `rng_ticket`: dùng để sinh `ticket_id = rng.gen()`
2. `rng_singer`: dùng trong **ECDSA nonce**: `k = rng.gen()`

Cả 2 bản sao có cùng quy luật, chỉ khác **seed ban đầu** (khởi tạo ở 2 chỉ số khác nhau).  
Vì vậy, cả hai sinh ra **cùng một dãy tuyến tính**, chỉ là bị **dịch pha**.

---

## Liên hệ với ECDSA
Trong ECDSA, với thông điệp `m` và chữ ký `(r, s)` ta có công thức:

```
s = k^{-1}(z + r d) mod n
```

suy ra:

```
k = a + B d (mod n)
```

trong đó:
- `a = z * s^{-1} mod n`
- `B = r * s^{-1} mod n`
- `z = sha256(m) mod n`

Như vậy, từ mỗi chữ ký, ta thu được một **hàm tuyến tính theo private key d**:
```
Ai(d) = ai + Bi d
```
và `Ai(d)` chính là nonce `ki`.

---

## Dãy RNG
Gọi dãy RNG là `f(t)`.

- Nonce: `ki = f(s + i)` với chỉ số bắt đầu bí mật `s`.
- Ticket: `ti = f(u + i)` với chỉ số bắt đầu bí mật `u`.

Giả sử **độ lệch pha** là `c = u - s`, thì ta có quan hệ tuyến tính:

```
f(x + c) = U f(x+1) + V f(x)
```

Trong đó `U, V` chỉ phụ thuộc vào `c`.

Áp dụng tại `x = s + i`:

```
ti = V * ki + U * k_{i+1} (mod n)
```

Thay `ki = Ai(d)` ta được:

```
ti = V * Ai(d) + U * A_{i+1}(d) (mod n)
```

---

## Giải hệ
Lấy 3 vé liên tiếp `ti` (cần là **3 số chẵn liên tiếp**) ⇒ được **3 phương trình** dạng trên.  
Khử `U, V` ⇒ thu được **1 phương trình bậc 2 theo d**:

```
F(d) = 0 (mod n)
```

Giải phương trình này cho ra 1–2 nghiệm ứng viên cho private key `d`.

---

## Kiểm tra nghiệm
Với mỗi nghiệm ứng viên `d`:
- Tính lại `k = ai + Bi d`
- Kiểm tra chữ ký `(r, s)`:
  ```
  r ?= x((ai + Bi d) * G) mod n
  ```

Nếu khớp ⇒ nghiệm đúng ⇒ tìm được private key thật.

---

## Script

``` python3
from os import environ
environ["TERM"] = "xterm"
from pwn import context, remote
from hashlib import sha256
from base64 import b64encode, b64decode
import json

context.log_level = "warning"
host = "0.cloud.chals.io"
port = int(19521)


def rec():
    return conn.recvlineS(False)

def send(tid, h, r, s):
    payload = {"ticket_id": tid}
    sig = r.to_bytes(32) + s.to_bytes(32)
    ticket = {
        "payload": payload,
        "signature": sig.hex()
    }
    conn.sendlineafter(b": \n", b64encode(json.dumps(ticket).encode()))

def parse(data):
    ticket = json.loads(b64decode(data))
    payload = ticket["payload"]
    tid = payload["ticket_id"]
    h = int.from_bytes(sha256(json.dumps(payload).replace(" ", "").encode()).digest())
    sig = bytes.fromhex(ticket["signature"])
    r = int.from_bytes(sig[:32])
    s = int.from_bytes(sig[32:])
    return tid, h, r, s

def option(choice):
    conn.sendlineafter(b"prize\n\n", str(choice).encode())


while True:
    conn = remote(host, port)

    option(1)
    tickets = [parse(rec())]

    for _ in range(3):
        option(2)
        send(*tickets[-1])
        output = rec()
        if not "ticket" in output:
            break
        tickets.append(parse(output.split()[-1]))

    if len(tickets) == 4:
        break

tid, h, r, s = zip(*tickets)

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
F = GF(p)
A = matrix(F, [
    [tid[1], -tid[0]],
    [tid[2], -tid[1]],
])
Y = vector(F, [
    tid[2],
    tid[3],
])
X = A.solve_right(Y)

R.<t,n,h1,h2,h3,h4,r1,r2,r3,r4,s1,s2,s3,s4,k1,k2,k3,k4,d> = F[]
eqs = [
    k1 * s1 - h1 - r1 * d,
    k2 * s2 - h2 - r2 * d,
    k3 * s3 - h3 - r3 * d,
    k4 * s4 - h4 - r4 * d,
    k3 - t * k2 + n * k1,
    k4 - t * k3 + n * k2,
]

t, n = map(int, X)
vals = dict(zip(R.gens()[:-5], (t, n) + h + r + s))

I = R.ideal([eq.subs(vals) for eq in eqs])
G = I.groebner_basis()
sol = {}
for g in G:
    if len(v := g.variables()) == 1:
        sol[str(v[0])] = -g.constant_coefficient()
d = sol["d"]

tid = int.from_bytes(sha256(b"I'd like the flag please").digest())
h = int.from_bytes(sha256(json.dumps({"ticket_id": tid}).replace(" ", "").encode()).digest())
r = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
s = int((h + r * d) % p)

option(2)
send(tid, h, r, s)
flag = conn.recvuntilS(b"}").split()[-1]
print(flag)

# FortID{W1nn3r_Winn3r_Ch1ck3n_D1nn3r_64277d4d7650896a}
```

---

## Flag
```
FortID{W1nn3r_Winn3r_Ch1ck3n_D1nn3r_64277d4d7650896a}
```
