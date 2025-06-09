## theartofwar
### Descripiton
![Description](description.png)

[main.py](main.py)

[output.txt](output.txt)

### Analyzed
1. Phân tích một chút về hàm tạo khóa
   - Chỉ để phi_N và e nguyên tố cùng nhau
2. Về hàm mã hóa:
   - Tạo ra e lần n và c cho nên có thể sử dụng định lý thặng dư Trung Hoa để giải quyết bài toán
3. Định lý thặng dư Trung Hoa
- Định lý: Cho $m_1,m_2,...,m_n$ các cặp đôi một nguyên tố cùng nhau $(m_i,m_j)=1$  và một hệ gồm $n$ phương trình
  
```math
x \equiv a_1\ (mod\ m_1)\\
x \equiv a_2\ (mod\ m_2)\\    
...\\
x \equiv a_n\ (mod\ m_n)\\
```
có một nghiệm duy nhất module $M$ với $M = m_1.m_2....m_n$
- Lấy $b_i = \frac{M}{m_i}$ và $b_i^{'} \equiv b_i^{-1}\ (mod\ m_i)$ thì ta tìm được nghiệm $x$ duy nhất bằng công thức
```math
x = \sum_{i=1}^n a_i.b_i.b_i^{'}\ (mod\ M)
```
- Ta xây dựng nghiệm $x$ theo tổng của các số hạng $t_i$ và $t_i$ đáp ứng các tiêu chí:
    - Đáp ứng phương trình chính nó : $t_i \equiv a_i(mod\ m_i)$
    - Là tích của các module $m_j$ với $j \ne i$ để tránh trường hợp trùng đồng dư với các $t_j$ khác
```math
t_i \equiv a_i\ (mod\ m_i)\\
t_i \equiv 0\ (mod \ m_j) \ \forall \ j \ne\ i
```
- Ta có: $t_i = a_i.b_i$ , tuy nhiên sau khi nhân với $b_i$ thì $t_i$ không còn đồng dư $a_i$ theo module $m_i$ nữa, cho nên ta cần tìm một số $k$ sao cho:
```math
a_i.b_i.k\equiv a_i\ (mod\ m_i)\\
\Rightarrow b_i.k \equiv 1\ (mod\ m_i)
```
- Mà ta có $(b_i,m_i)=1$ cho nên tìm $k$ là hoàn toàn có thể $(b_i^{'})$
Cho nên công thức tìm nghiệm chính là:
```math
x = \sum_{i=1}^n t_i \ (mod\ M)= \sum_{i=1}^n a_i.b_i.b_i^{'}\ (mod\ M)
```
  
### Solution
