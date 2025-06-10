# rubix-cube
## Description
![description](description.png)

[rubixcube.py](rubixcube.py)

[cube_scrambled.txt](cube_scrambled.txt)

## Analyzed
Phân tích một chút file `rubixcube.py`, ta thấy lớp `RubiksCube` với hai phần quan trọng:
1. `apply_moves(move)` : quay mặt khối theo kí hiệu (“U”, “L”, “F”, “B’”, “D’”, “R’”)
2. `get_flat_cube_encoded()`: xuất ra chuỗi kí tự mã hóa trạng thái hiện tại của toàn bộ 54 miếng.

Đọc file `cube_scrambled.txt`, đó là trạng thái của rubik sau 2 lượt tráo:
1. Lượt đầu tráo xong được ẩn chính là FLAG
2. Lượt hai được sinh công khai bằng đoạn code với `seed = 42` và danh sách `moves` ổn định
Cho nên nếu ta tạo đối tượng `RubiksCube` rồi gán thẳng `cube.faces = scrambled_state`, tức là khối đang ở sau cả hai lượt tráo

## Solution
- Ta có được ý tưởng nếu quay lại liên tiếp 4 lần thì nó sẽ trở thành vị trí cũ, cho nên ta chỉ cần quay thêm 3 lần là sẽ quay ngược lại
- Đầu tiên ta sinh lại chính xác chuỗi xáo thử 2:
```python
moves = ["U","L","F","B'","D'","R'"]
random.seed(42)
scramble2 = []
for _ in range(20):
    order = [random.randint(0,5) for _ in range(50)]
    for idx in order:
        scramble2.append(moves[idx])
```
- Sau đó ta duyệt ngược lại từ cuối lên đầu mảng `scramble2`, với mỗi `move` ta áp dụng chính `move` đó 3 lần:
```python
for mv in reversed(scramble2):
    for _ in range(3):
        cube.apply_moves(mv)
```
- Cuối cùng ta gọi `cube.get_flat_cube_encoded()` để nhận về Flag
  
```python
print(f"tjctf{{{cube.get_flat_cube_encoded()}}}")
```
- Và đây là cả đoạn script:
```python
import copy
import random
import numpy as np
import ast

class RubiksCube:
    def __init__(self):
        self.faces = {
            'U': [['⬜'] * 3 for _ in range(3)],
            'L': [['🟧'] * 3 for _ in range(3)],
            'F': [['🟩'] * 3 for _ in range(3)],
            'R': [['🟥'] * 3 for _ in range(3)],
            'B': [['🟦'] * 3 for _ in range(3)],
            'D': [['🟨'] * 3 for _ in range(3)]
        }

    def _rotate_face_clockwise(self, face_name):
        face = self.faces[face_name]
        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[2-j][i]
        self.faces[face_name] = new_face

    def _rotate_face_counter_clockwise(self, face_name):
        face = self.faces[face_name]
        new_face = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                new_face[i][j] = face[j][2-i]
        self.faces[face_name] = new_face

    def get_flat_cube_encoded(self):
        flat = list(np.array(self.faces).flatten())
        # encode only emoji chars
        return "".join([chr(ord(ch) % 94 + 33) for ch in str(flat) if ord(ch) > 256])

    def U(self):
        self._rotate_face_clockwise('U')
        temp = self.faces['F'][0]
        self.faces['F'][0] = self.faces['R'][0]
        self.faces['R'][0] = self.faces['B'][0]
        self.faces['B'][0] = self.faces['L'][0]
        self.faces['L'][0] = temp

    def L(self):
        self._rotate_face_clockwise('L')
        temp = [self.faces['U'][i][0] for i in range(3)]
        for i in range(3): self.faces['U'][i][0] = self.faces['B'][2-i][2]
        for i in range(3): self.faces['B'][2-i][2] = self.faces['D'][i][0]
        for i in range(3): self.faces['D'][i][0] = self.faces['F'][i][0]
        for i in range(3): self.faces['F'][i][0] = temp[i]

    def F(self):
        self._rotate_face_clockwise('F')
        temp = self.faces['U'][2].copy()
        for i in range(3): self.faces['U'][2][i] = self.faces['L'][2-i][2]
        for i in range(3): self.faces['L'][i][2] = self.faces['D'][0][i]
        for i in range(3): self.faces['D'][0][2-i] = self.faces['R'][i][0]
        for i in range(3): self.faces['R'][i][0] = temp[i]

    def D_prime(self):
        self._rotate_face_counter_clockwise('D')
        temp = self.faces['F'][2]
        self.faces['F'][2] = self.faces['R'][2]
        self.faces['R'][2] = self.faces['B'][2]
        self.faces['B'][2] = self.faces['L'][2]
        self.faces['L'][2] = temp

    def R_prime(self):
        self._rotate_face_counter_clockwise('R')
        temp = [self.faces['U'][i][2] for i in range(3)]
        for i in range(3): self.faces['U'][i][2] = self.faces['B'][2-i][0]
        for i in range(3): self.faces['B'][2-i][0] = self.faces['D'][i][2]
        for i in range(3): self.faces['D'][i][2] = self.faces['F'][i][2]
        for i in range(3): self.faces['F'][i][2] = temp[i]

    def B_prime(self):
        self._rotate_face_counter_clockwise('B')
        temp = self.faces['U'][0].copy()
        for i in range(3): self.faces['U'][0][i] = self.faces['L'][i][0]
        for i in range(3): self.faces['L'][i][0] = self.faces['D'][2][2-i]
        for i in range(3): self.faces['D'][2][i] = self.faces['R'][i][2]
        for i in range(3): self.faces['R'][i][2] = temp[2-i]

    def apply_moves(self, move):
        # single move without spaces
        if move == 'U': self.U()
        elif move == "L": self.L()
        elif move == "F": self.F()
        elif move == "D'": self.D_prime()
        elif move == "R'": self.R_prime()
        elif move == "B'": self.B_prime()
        else:
            print(f"Ignored unknown move {move}")

if __name__ == '__main__':
    with open(r'E:\CTF\TJCTF2025\Reverse\rubix\cube_scrambled.txt','r',encoding='utf-8') as f:
        state = ast.literal_eval(f.read())
    cube = RubiksCube()
    cube.faces = state
    
    moves = ["U","L","F","B'","D'","R'"]
    random.seed(42)

    scramble2 = []
    for _ in range(20):
        order = [random.randint(0,5) for _ in range(50)]
        for idx in order:
            scramble2.append(moves[idx])

    for mv in reversed(scramble2):
        for _ in range(3):
            cube.apply_moves(mv)

    print(f"tjctf{{{cube.get_flat_cube_encoded()}}}")
```
Và flag chính là:
```plaintext
tjctf{G>BGG@BBGA>B>@B??>@G?@B??B>>?GA>@G@ABB@A?AA?@?AA>AG>G@}
```
