# Free Candy [crypto] – Writeup

## Ý tưởng chính

Bài này khai thác **RNG bị tái sử dụng** trong ECDSA.

- Có một RNG duy nhất nhưng dịch vụ tạo ra **2 bản copy**:
  1. `rng_ticket` → sinh `ticket_id`.
  2. `rng_singer` → sinh nonce `k` cho ECDSA.
- Cả hai copy chạy cùng một dãy **truy hồi tuyến tính** (linear recurrence sequence), chỉ khác nhau ở **offset**.

---

## ECDSA nhắc lại

Với thông điệp `m` và chữ ký `(r, s)`:

\[
s \equiv k^{-1}(z + r d) \pmod{n}
\]

Suy ra:

\[
k \equiv a + B d \pmod{n}
\]

Trong đó:

- \(a = z s^{-1} \pmod{n}\)
- \(B = r s^{-1} \pmod{n}\)
- \(z = \text{sha256}(m) \pmod{n}\)
- \(d\) là private key

→ Mỗi chữ ký cho ta một phương trình **tuyến tính theo \(d\)**:

\[
A_i(d) = a_i + B_i d = k_i
\]

---

## Liên hệ Ticket ↔ Nonce

- RNG sinh ra:
  - Nonces: \(k_i = f(s+i)\)
  - Tickets: \(t_i = f(u+i)\)

- Với offset \(c = u - s\), tồn tại hằng số \(U, V\) sao cho:

\[
f(x+c) = U f(x+1) + V f(x)
\]

- Thay \(x = s+i\):

\[
t_i = V k_i + U k_{i+1} = V A_i(d) + U A_{i+1}(d) \pmod{n}
\]

---

## Cách giải

1. Lấy **3 vé liên tiếp** \(t_i, t_{i+1}, t_{i+2}\).
2. Loại bỏ \(U, V\) → thu được một phương trình bậc 2 theo \(d\):

   \[
   F(d) = 0 \pmod{n}
   \]

3. Giải phương trình → thu được 1–2 nghiệm \(d\).
4. Kiểm tra nghiệm bằng cách verify ECDSA:

   \[
   r_i \stackrel{?}{=} x\big((a_i + B_i d)G\big) \pmod{n}
   \]

5. Nếu đúng → khôi phục được private key.

---

## Khó khăn

- Server chỉ phát **ticket khi ticket_id là số chẵn**.
- Cần **3 vé chẵn liên tiếp** → xác suất chỉ là \(1/8\).
- Do đó phải brute-force trong vài phút để lấy đủ dữ liệu.

---

## Kết quả

Sau khi thu thập được 3 vé chẵn liên tiếp và giải phương trình, tìm ra private key → sign → lấy flag:

