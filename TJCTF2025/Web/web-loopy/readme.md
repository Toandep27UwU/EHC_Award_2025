![image](https://github.com/user-attachments/assets/959048ba-851d-48ae-bbad-e8edd278995b)

# **ANALYZE**

Đầu tiên khi đến với chall , nhìn qua giao diện của trang web thì ta thấy có 1 ô input để ta có thể nhập url vào để trang web crawl data html về , 
và ta có thể nghĩ ngay đến lỗ hổng SSRF.
![image](https://github.com/user-attachments/assets/d1cbd907-43c1-4e43-9e7a-a05248b93c84)

lỗ hổng SSRF là lỗ hổng ta tận dụng khả năng của server trong việc gửi yêu cầu HTTP đến các địa chỉ khác, từ đó truy cập hoặc tương tác với các tài nguyên 
mà đáng lẽ chỉ server mới có quyền truy cập.
![image](https://github.com/user-attachments/assets/43785324-22d5-494a-b53b-83c72bd6a060)

Và yêu cầu của đề bài là :"Can you access the admin page? Running on port 5000"
Tôi sẽ thử mới địa chỉ localhost:5000/admin để thử kiểm tra : 
![image](https://github.com/user-attachments/assets/32c2687a-07a5-46fe-a3d6-f426a2f8eda2)

vậy có vẻ là trang web này đã cố gắng filter để chống SSRF : 
`"Access denied. URL parameter included one or more of the following banned keywords: [::], 017700000001, 0.0.0.0, ffff, ::1, 2130706433, local, 127"`
Nhưng tất nhiên chúng ta vẫn sẽ còn nhiều cách khác để có thể vượt qua lớp filter này : 

Và thật ra trang web chỉ cố chặn cái 'localhost' nhưng đã bỏ quên 1 thứ quan trọng , ta có thể dùng : `http://0:`để thay thế cho `localhost`
![image](https://github.com/user-attachments/assets/d2f9878e-db5d-47fc-b61c-294094431569)


# **EXPLOIT**
vậy nên payload cuối cùng của bài sẽ là : 
```
http://0:5000/admin
```
![image](https://github.com/user-attachments/assets/4b0a4b7a-6c3f-416b-9f56-740cdca5dc2d)

# **FLAG**
`tjctf{i_l0v3_ssssSsrF_9o4a8}`
