# Free Candy [crypto] - Writeup (Tiếng Việt)

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

👉 Như vậy, từ mỗi chữ ký, ta thu được một **hàm tuyến tính theo private key d**:
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

## Vấn đề thực tế
Server **chỉ cấp ticket mới nếu ticket_id là số chẵn**.  
Mà ta lại cần **3 ticket chẵn liên tiếp** để giải được hệ ⇒ xác suất chỉ **1/8** để gặp chuỗi “may mắn” này.

Do đó, phải spam khá nhiều request cho đến khi lấy được 3 vé chẵn liên tiếp. Sau khi có, chạy solver sẽ ra key và sign flag.

---

## Flag
```
FortID{W1nn3r_Winn3r_Ch1ck3n_D1nn3r_64277d4d7650896a}
```
