# Can you see through the star

<img width="1378" height="543" alt="image" src="https://github.com/user-attachments/assets/8cd5f368-9a31-4a0c-a277-51f96df5c002" />

Kiểm tra thì đây là pe32 và sử dụng .NET nên sử dụng dnspy32

<img width="721" height="515" alt="image" src="https://github.com/user-attachments/assets/4dbc8a75-57c0-4ae3-8ca3-d751b221a1f7" />

Nhìn vào đoạn code thì có vẻ khi chạy sẽ hiện lên giao diện, ấn vào button thì nó sẽ cho ra flag:

<img width="1636" height="819" alt="image" src="https://github.com/user-attachments/assets/0a486f5d-a890-4e72-895b-234be453e221" />

Flag được ghép từ `FLAG-<maskedTextBox1>vc<button1>`, tiếp theo thì đi tìm giá trị của mấy cái đó là gì là ra

<img width="674" height="610" alt="image" src="https://github.com/user-attachments/assets/cf4a9a01-ce7f-41fc-af42-3bbf0764684f" />

Có thể dễ thấy flag đã được gán sẵn rồi nên flag là:

`FLAG-maskedTextBox1vcbutton1`

