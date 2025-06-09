![image](https://github.com/user-attachments/assets/064449cc-e048-4e66-bd27-067754825a68)

Đề bài cho 2 file gồm file chall là ELF64 và config.dat:

![image](https://github.com/user-attachments/assets/e88f485d-a7c9-4dd1-a6c6-e49514bdc727)

Không hiểu sao khi tôi chạy chall thì luôn trả lại "Validation failed."

![image](https://github.com/user-attachments/assets/3bf7fb35-e7f6-4fbd-b3d2-66e1f6257c0d)

Mở ở trong ida thì nhìn hơi lằng ngoằng

![image](https://github.com/user-attachments/assets/b3634024-0605-4eb4-ab0b-cd37e2f6ca1f)

Và tôi debug thử, do vấn đề nằm ở đây nên tôi để tạm cái breakpoint ở đó:

![image](https://github.com/user-attachments/assets/38137818-b698-41e5-aa4c-74a67b619c75)

Kiểm tra thì biến v28 trả lại kết quả là 6 thay vì 7, thế nên nó nhảy vào else:

![image](https://github.com/user-attachments/assets/46769c3b-95f0-4d7a-b715-31a0575a1401)

Tôi đổi flag ZF thành giá trị 1 để ép chương trình chạy vào if 

![image](https://github.com/user-attachments/assets/351d3b57-32c9-4bc5-b235-2a06eaa7b475)

Trong đây thì có gọi đến hàm `sub_557554537273` với các tham số gồm v13 là giá trị của 1 số hex nằm trong file config.dat

![image](https://github.com/user-attachments/assets/233c518c-9a46-4f10-a8e3-f611427c2084)

![image](https://github.com/user-attachments/assets/3f68008e-443c-4342-b86a-7502cfe4ad03)

Tham số thứ 2 là 9, tham số thứ 4 là 4, tham số thứ 3 là `k3y!` có ở trong config.dat:

![image](https://github.com/user-attachments/assets/33254b8e-990e-41a3-92db-1e13ba695e3a)

Và trong hàm `sub_557554537273` thì nó đang làm gì đó, thay vì ngồi đọc thì tôi cho nó chạy xem nó đang làm gì

![image](https://github.com/user-attachments/assets/8083af78-741f-4b1e-b1d4-1e83b1915788)

Sau khi chạy 7 lần vòng lặp thì ra được `c0nf1g_`, mấy cái ở dưới là 0, không có gì, nhưng mà vòng lặp nó để là 9 nên vẫn chạy tiếp

![image](https://github.com/user-attachments/assets/463770b0-f88a-4143-864d-273caee966e6)

Nếu để chạy đúng 9 vòng thay vì 7 vòng thì flag sẽ sai do nó xor với cả mấy cái 0 ở dưới

Để thoát vòng lặp thì chỉnh là cái jb, tức là chỉnh cái flag CF thành 0 để thoát khỏi vòng lặp:

![image](https://github.com/user-attachments/assets/777dffc8-9f44-439b-b5fd-99a4e1a931f0)

Lúc này thì flag được ghép từ v13 và v10, cái v10 thì đơn giản, xem đoạn code ở trên

![image](https://github.com/user-attachments/assets/55063ddf-a953-47a6-97db-55248845dc84)

![image](https://github.com/user-attachments/assets/1a7fe042-ec63-49d8-9d02-faaa55a88cd6)

Flag là `tjctf{c0nf1g_r3v3rse}`


