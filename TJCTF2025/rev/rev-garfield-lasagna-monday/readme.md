![image](https://github.com/user-attachments/assets/a2a632e2-bfb1-492d-8ee1-7174fce43710)

# **ANALYZE**

Và chúng ta đã tìm thấy 1 bài web ở trong mục rev , thì chỉ cso thẻ kết luận , đây chính là webasembly -))
![image](https://github.com/user-attachments/assets/4dc7fc53-15f7-48c2-9fe6-fb75f12208f4)


Và tôi đã quyết định bật dev tool lên , mở phần network , và thử điền bừa để xem có sự thay đổi j ở các gói tin

Tôi đã phát hiện ra nó đa xuất hiện gói tin challange.wasm như trên ảnh : 

![image](https://github.com/user-attachments/assets/8bb6bfac-b78b-4c8f-9588-3a054f771e6a)

![image](https://github.com/user-attachments/assets/95322f24-2577-4196-9feb-3ce2916d32f0)

vì không có kinh nghiệm sâu về asembly , nên tôi đã nhờ đến chatgpt làm thay nhiệm vụ reverse .

Dùng tool wasm2wat để dịch .wasm → .wat:

Và tôi đã nhận được kết quả sau khi nhờ chatgpt làm việc : 

```
blue|tuxedo|dance|chaos|pancakes
```
cái này tượng trưng cho 5 vị trí đàu tiên để chúng diền vào , có thể điền ngẫu nhiên ở các ô còn lại

![image](https://github.com/user-attachments/assets/da3e7051-5edd-4ffe-88c2-7255a95e90ee)


# **FLAG**
```
tjctf{w3b_m4d_libs_w4sm}
```
