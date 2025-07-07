![image](https://github.com/user-attachments/assets/9b67fc82-4f5f-47f9-a477-96d3bd4801ed)

# ANALYZE

![image](https://github.com/user-attachments/assets/947d4260-7d3d-4e6d-b43f-472fa42444d9)

Khi truy cập vào bài lab , ta thây 1 form đăng nhập , ko có gì quả nối bật , vậy nên ta sẽ chuyển qua đọc source code

```
from flask import Flask, redirect, render_template, request, url_for
from secret import FLAG

app = Flask(__name__)


def complex_custom_hash(data_string):
    if not isinstance(data_string, str):
        raise TypeError("Input must be a string.")

    data_bytes = data_string.encode("utf-8")

    P = 2**61 - 1
    B = 101

    hash_val = 0

    for byte_val in data_bytes:
        hash_val = (hash_val * B + byte_val) % P

    length_mix = (len(data_bytes) * 123456789) % P
    hash_val = (hash_val + length_mix) % P

    chunk_size = 40
    num_chunks = 64 // chunk_size

    folded_hash = 0
    temp_hash = hash_val

    for _ in range(num_chunks):
        chunk = temp_hash & ((1 << chunk_size) - 1)
        folded_hash = (folded_hash + chunk) % (1 << chunk_size)
        temp_hash >>= chunk_size

    final_small_hash = folded_hash

    scrambled_hash = 0
    for _ in range(3):
        scrambled_hash = (
            final_small_hash ^ (final_small_hash >> 7) ^ (final_small_hash << 3)
        ) & ((1 << chunk_size) - 1)
        final_small_hash = scrambled_hash

    return f"{scrambled_hash:04x}"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username != password and complex_custom_hash(
            password
        ) == complex_custom_hash(username):
            return FLAG
        return redirect(url_for("home"))

    url_for("static", filename="style.css")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
```
Đầu tiên 

```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username != password and complex_custom_hash(password) == complex_custom_hash(username):
            return render_template("flag.html", flag=SECRET_FLAG)
```
Điều Kiện để xác thực thành công là : 

1. `username != password`
2. `hash(username) == hash(password)` với hàm `complex_custom_hash`

Nếu thỏa cả 2, trả về `flag.html`.

Tiếp đến chính là 1 hàm băm 

```python
def complex_custom_hash(s: str) -> str:
    seed = 0x1337
    scrambled_hash = seed
    for c in s:
        scrambled_hash ^= ord(c)
        scrambled_hash = (scrambled_hash << 5 | scrambled_hash >> 3) & 0xFFFFFFFF
        scrambled_hash += 0x4242
        scrambled_hash ^= 0xDEADBEEF
    return f"{scrambled_hash:04x}"
```

- Dùng nhiều phép toán XOR, dịch bit trái/phải, cộng thêm hằng số cố định.
- Cuối cùng trả về chỉ **4 ký tự hex**:
  ```python
  return f"{scrambled_hash:04x}"
  ```
  → Tức là chỉ có `2^16 = 65536` giá trị có thể ⇒ **hash rất yếu và dễ va chạm (collision)**.

# EXPLOIT

Bây giờ chúng ta sẽ tiến hành tìm 2 chuỗi khác nhau có cùng giá trị `complex_custom_hash`

```python
import random, string
from main import complex_custom_hash   # đã cho sẵn

seen = {}

while True:
    s = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    h = complex_custom_hash(s)
    if h in seen and seen[h] != s:
        print(f"[+] Found collision:\nUsername: {seen[h]}\nPassword: {s}\nHash: {h}")
        break
    seen[h] = s
```

Và kết quả trả về  : 
```
[+] Found collision:
Username: fCBs2h
Password: 108syk
Hash: 57b4ff9a58
```

Bước cuối cùng thì ta chỉ cần đăng nhập với 2 trường tài khoản và mật khẩu vừa tìm được . 

![image](https://github.com/user-attachments/assets/7af43751-97ea-4a6a-ab7d-ec2efde5dc91)


# FLAG

```
Blitz{b1r7hd4y_p4r4d0x_3475_5h177y_h45h35_l1k3_7h15}
```
