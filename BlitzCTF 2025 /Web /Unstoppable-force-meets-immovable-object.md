![image](https://github.com/user-attachments/assets/67c3c2fa-46fd-4b20-a76c-6a3ceae9becc)

# ANALYZE

![image](https://github.com/user-attachments/assets/a744275e-cb01-408c-ac26-7812c1091289)


Bài này khi ta truy cập vào chall , thì ta thấy có 1 form đăng nhập , ta sẽ chuyển sang kiểm tra source code :

```
from flask import Flask, redirect, render_template, request, url_for
from secret import FLAG

app = Flask(__name__)

NOT_PASSWORD = "P@ssword@123"


def immovable_object(data, block_size=32):
    if len(data) % block_size != 0:
        data += b"\0" * (block_size - (len(data) % block_size))

    h = 0
    for i in range(0, len(data), block_size):
        block = int.from_bytes(data[i : i + block_size], "big")
        h ^= block

    return h


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form["password"]
        unstopabble_force = immovable_object(password.encode("utf-8"))
        if password != NOT_PASSWORD and unstopabble_force == immovable_object(
            NOT_PASSWORD.encode()
        ):
            return FLAG
        return redirect(url_for("home"))

    url_for("static", filename="style.css")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

```

Route / chứa đoạn code xử lý:
```
if request.method == "POST":
    password = request.form["password"]
    unstopabble_force = immovable_object(password.encode("utf-8"))
    if password != NOT_PASSWORD and unstopabble_force == immovable_object(NOT_PASSWORD.encode()):
        return FLAG
```

Điều kiện cấp FLAG:
password phải khác NOT_PASSWORD = "P@ssword@123"

Hash của password (qua immovable_object) phải giống hash của NOT_PASSWORD


```
def immovable_object(data, block_size=32):
    if len(data) % block_size != 0:
        data += b"\0" * (block_size - (len(data) % block_size))

    h = 0
    for i in range(0, len(data), block_size):
        block = int.from_bytes(data[i : i + block_size], "big")
        h ^= block

    return h
```
Hàm pad input đến độ dài chia hết cho 32 byte

Sau đó chia thành các block 32 byte và thực hiện XOR liên tục

Đây là một dạng hash rất đơn giản → dễ bị collision


## Ý tưởng khai thác : 

Hàm immovable_object sử dụng XOR:

A ⊕ A = 0, A ⊕ B ⊕ B = A

Ta có thể:

Thay đổi 1 byte trong NOT_PASSWORD để làm nó khác đi

Sau đó thêm 1 block có cùng thay đổi để khôi phục lại giá trị hash

=> Điều kiện được thỏa mãn:
password != NOT_PASSWORD

immovable_object(password) == immovable_object(NOT_PASSWORD)


# EXPLOIT 

```
import requests

def gen_payload():
    x = b'P@ssword@123' + b'\x00' * (32 - len(b'P@ssword@123'))
    payload = bytearray(x)
    payload[0] ^= 1  # Thay đổi 1 bit

    # Thêm block bù XOR lại bit đã thay đổi
    padding = bytearray(32)
    padding[0] = 1
    return payload + padding

url = 'https://ufmio-n1sj9nsb.blitzhack.xyz/'

password = gen_payload()
resp = requests.post(url, data={
    'password': password.decode(errors='ignore')
})

print(resp.text)  # FLAG hiển thị nếu khai thác thành công
```

# FLAG 

```
blitz{60nn4_b3_4_b16_c0ll1510n_wh3n_un570pp4bl3_f0rc3_m3375_1mm0v4bl3_0bj3c7}
```



