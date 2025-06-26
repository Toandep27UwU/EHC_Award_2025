# Tổng Quan

![image](https://github.com/user-attachments/assets/e54ef711-cca8-4a71-8790-86a8d002a13c)

Thử thách này cho tôi 1 file elf64

![image](https://github.com/user-attachments/assets/c197b6b0-4c15-42fb-8589-a0132ca1d648)

Khi chạy file này thì có yêu cầu người dùng nhập vào flag và dĩ nhiên tôi chưa biết flag của nó là gì

![image](https://github.com/user-attachments/assets/43ea0e0f-6f33-4f0b-98b8-1879526c5816)

Đưa vào ida thì nó có dạng sau

![image](https://github.com/user-attachments/assets/e54bd656-6a52-44f3-bdf2-4f489dda5ecf)

Chương trình check giá trị của v7, tức là dữ liệu do người dùng nhập vào bằng cách sử dụng hàm compute_secret(v7), tôi tiếp tục đào sâu vào hàm đấy

![image](https://github.com/user-attachments/assets/03373522-f747-4ebc-98ad-01aa7ca480e6)

Hàm này có dạng như sau

![image](https://github.com/user-attachments/assets/befc3201-35cb-423e-989f-04b285dfac32)

Có thể hình dung chỗ code này theo biểu thức như sau 

![image](https://github.com/user-attachments/assets/cc5bea95-c987-4157-8127-80ac29f42af6)

Ở FLAG thì là array gồm những giá trị này ở dạng decimal:

![image](https://github.com/user-attachments/assets/fd7fd6b1-419c-4a77-af8b-979bb6473b8a)

# Khai Thác

Từ đó tôi suy ra được hệ phương trình gồm 40 ẩn, mỗi ẩn là 1 kí tự của flag, để giải nhiều ẩn thì sử dụng thư viện z3 trong python, tôi có đoạn code bé bé xinh xinh do chatgpt làm hộ ở đây:

```
from z3 import *

flag_data = [
    68303, 136428, 204420, 272424, 339770, 407724, 472591, 539952,
    606861, 673840, 745943, 806808, 870272, 935480, 1006035, 1069664,
    1136637, 1194768, 1268421, 1329480, 1398369, 1450988, 1536630,
    1611600, 1658100, 1741896, 1761534, 1863512, 1917248, 1990020,
    2028299, 2134720, 2165955, 2228768, 2308565, 2320200, 2453174,
    2527456, 2531217, 2534960
]

FLAG_LENGTH = 40

solver = Solver()

s = [BitVec(f's_{i}', 8) for i in range(FLAG_LENGTH)]


for i in range(FLAG_LENGTH):
 
    current_sum = Sum([
        (i + 1) * (j + 1) * ZeroExt(16, s[j])
        for j in range(FLAG_LENGTH)
        if i != j  
    ])

    solver.add(current_sum == flag_data[i])

for char_var in s:
    solver.add(And(char_var >= 0x20, char_var <= 0x7e))


if solver.check() == sat:

    model = solver.model()

    secret_str = "".join([chr(model[char].as_long()) for char in s])

    print(f"flag: {secret_str}")
else:
    print("Khong biet lam")
```

Chạy đoạn code trên là ra được flag:

![image](https://github.com/user-attachments/assets/e7cee188-a5f6-43d4-98d5-6a5662b7a980)

