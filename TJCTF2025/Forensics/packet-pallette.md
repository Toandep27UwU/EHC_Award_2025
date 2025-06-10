![image](https://github.com/user-attachments/assets/f4cc4592-92e7-44c7-9f02-37d47887e837)

![image](https://github.com/user-attachments/assets/ea77f150-4e25-41ad-81dc-bee046136ea6)
khi mình mở file này trong HxD thì thấy nó có header của file png. Và mình đã thử dùng binwalk để xem hình ảnh này có gì đặc biệt

khi binwalk ra mình k thấy gì nên tiếp tục mở file này trong wireshark.
![image](https://github.com/user-attachments/assets/999d1b0f-fe9a-46ea-a14f-55580c399232)
![image](https://github.com/user-attachments/assets/9df1e5eb-8c2d-44a0-ac8c-747de3d8a341)

mình có để ý các packet của nó đều có các kí tự như "zizi" và "USB" ở đầu. Khả năng nó đã bị thêm vào và đã làm hỏng file ảnh 
thử trích xuất playload tcp : 

tshark -r chall.pcapng -Y "tcp" -T fields -e tcp.payload > payload.txt

để ý các kết quả của mỗi payload ( mỗi đoạn là một packet ) thì chính xác nó đã bị lặp lại đoạn "55534...01f4"

![image](https://github.com/user-attachments/assets/c0da1b59-ae4d-4a27-9987-a93f882ec7fa)

mình có lấy đoạn packet thứ 2 để decode thì mình biết được đoạn hex bị lặp lại mỗi đầu packet chính là "55534...01f4"

và sau khi xoá phần thừa đi và nối các đoạn vào với nhau ta sẽ ra được ảnh chứa flag

![image](https://github.com/user-attachments/assets/6de41d1f-637a-4c4f-86f7-8278a8a584ba)

Flags : tjctf{usb1p_f13g_1ns1d3_3_pr0t0c0l}
