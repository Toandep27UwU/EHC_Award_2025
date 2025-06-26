![image](https://github.com/user-attachments/assets/552164c1-a7c1-43ce-98af-576dd32fe9e4)
 đầu tiên mình có kiểm tra loại file thì thấy đây là một file ELF 64-bit, một loại file binary cho Linux
 sau đó mình có chạy thử nhưng không nhận đc flag .

 mình mở nó trên IDA để kiểm tra các fuction của nó
![image](https://github.com/user-attachments/assets/7c390155-7ea8-4194-bc25-758a55357a71)
lúc này mình k thấy nó có hàm main thêm cả không có tên biến rõ ràng nên nó đang được viết theo kiểu **assembly**

đầu tiên mình sẽ xem hàm **_start** trước,ngay tại đây, hàm _start gọi **system_write** để in ra dòng **"give me the secret flag"**
![image](https://github.com/user-attachments/assets/2ac440c2-2e6d-435d-aba1-df1eea205270)

ngay sau đó, nó lại tiếp tục gọi **system_read** để lấy chuỗi mà người dùng nhập vào với tối đa 45 byte **(edx, 2Dh)** rồi lưu vào stack tại **rsp**. Và giá trị trả về sẽ được lưu trong rax là số byte đọc được

tiếp đó nó sẽ gọi hàm compute_secret để kiểm tra input được nhập vào, nếu khớp data nó sẽ trả về flag.
![image](https://github.com/user-attachments/assets/86f3728c-7d7d-42e9-b25b-636281d3bed5)

mình sẽ chuyển tới hàm compute_secret để kiểm tra xem.

![image](https://github.com/user-attachments/assets/f09ef10c-5f0c-4dec-a3bb-66eea0ad24ed)

tại đây, 2 biến là var_8 và var_10 đang được khởi tạo và var_8 đc gán gtri là 0xFFFFFFFFFFFFFFFF hay là -1 (2's complement ) và var_10 đc gán giá trị bằng 0
![image](https://github.com/user-attachments/assets/c58767a5-137f-444f-ae87-80bc59c368a0)

dựa vào đây ta cũng có thể thấy được v3 là var_10 còn v4 chính là var_8, tại đây chúng ta đang thấy sử dụng vòng lặp với v3 chạy từ 0-40 và v4 chạy từ 0-39

tại đây, mình sẽ nói qua vai trò của từng biến, trước hết chính là **v4** : đây là chỉ số của mảng FLAG[], tại vì nó sẽ ứng với từng phần tử của mảng FLAG[].
và khi nó kiểm tra FLAG[v4] != 0 thì nó sẽ return lại giá trị 0 và nếu  FLAG[v4] == 0 nó sẽ tiếp tục kiểm tra và đến khi tất cả đều đúng nó sẽ return 4919.

**v3** : được khởi tạo từ 0 và chạy tới 40 và nó duyệt input của người dùng. Nó ảnh hưởng trực tiếp tới FLAG[v4] theo công thức : **"FLAG[v4]-=(unsigned __int8)*(_QWORD *)(a1 + v3)*v1;"**

với mỗi **FLAG[v4]** bị thay đổi bằng phép trừ theo input trong vòng lặp và với mọi FLAG[v4] == 0 sau khi qua các bước xử lí thì sẽ điều kiện sẽ thành công.


và tiếp theo, mình sẽ trích xuất data FLAG 
![image](https://github.com/user-attachments/assets/4e528564-1809-4f46-b568-897037985b53)


nhưng hiện tại để nguyên như vậy rất khó hiểu nên mình convert sang array 
![image](https://github.com/user-attachments/assets/8e3dd0b6-9e4b-4539-9c6d-7353d7703245)
![image](https://github.com/user-attachments/assets/51875222-5e69-4b37-8e1e-32be5f9554a6)

vì giá trị của v3 duyệt qua input của người dùng từ 0-40 nên ta sẽ lấy 41 phần tử trong mảng
![image](https://github.com/user-attachments/assets/782ee388-53cc-4fea-83e0-40729fb65c0a)
lúc này có vẻ các giá trị đều dễ nhìn hơn rồi, mình làm thêm bước nữa là ấn **H** thì các giá trị từ **hexadecimal** sẽ chuyển qua **decimal** 
sau đó chúng ta chỉ cần lấy chúng để reverse flag đúng từ FLAG[].

```
from z3 import *



flag_data = [
    68303,
    136428,
    204420,
    272424,
    339770,
    407724,
    472591,
    539952,
    606861,
    673840,
    745943,
    806808,
    870272,
    935480,
    1006035,
    1069664,
    1136637,
    1194768,
    1268421,
    1329480,
    1398369,
    1450988,
    1536630,
    1611600,
    1658100,
    1741896,
    1761534,
    1863512,
    1917248,
    1990020,
    2028299,
    2134720,
    2165955,
    2228768,
    2308565,
    2320200,
    2453174,
    2527456,
    2531217,
    2534960
]
solver = Solver()

s = [BitVec(f's_{i}',8) for i in range(40)]


def main():
    for i in range(40):
        term = 0
        for j in range(40):
            if i == j:
                continue
            term += (j*i +j +i + 1) * ZeroExt(8,s[j])

        solver.add(term == flag_data[i])
    for byte in s:
        solver.add(byte >= 0x20, byte <= 0x7E)    
    if solver.check() == sat:
        model = solver.model()
        secret_bytes = []
        for i in range(40):
            byte_val = model[s[i]].as_long()
            secret_bytes.append(byte_val)
        secret_str = ''.join(chr(b) for b in secret_bytes)
        print(f"Secret: {secret_str}")

if __name__ == "__main__":
    main()
```
script sử dụng thư viện z3 và tính theo công thức `FLAG[i] - (i+1)*(0+1)*s[0] - (i+1)*(1+1)*s[1] - ... - (i+1)*(44+1)*s[44] = 0`               

và khi mình đưa các giá trị vô và chạy script thì nó sẽ trả về secret và lấy được flag 
![image](https://github.com/user-attachments/assets/e1b5dcc2-b041-4994-a03b-0d29ca133de6)


**Flag  :  GPNCTF{nic3_noW_YoU_UnD3R5tAND_4SSEm81Y}**
