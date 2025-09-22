# Writeup: giải bài “brush / farthest distance” và trích flag từ `flag_input.txt`

> TL;DR: Bài toán sinh ảnh ASCII bằng cách chọn lần lượt số **xa nhất** so với các số đã chọn trong đoạn \([1, 2^n-1]\) (seed: `1` và `2^n-1`). Quy trình này tương đương việc **chẻ đôi các khoảng dài nhất** và lấy **trung điểm kiểu dyadic** theo từng tầng. Nhờ vậy có thể tính phần tử thứ `k` **không cần mô phỏng** toàn bộ.

---

## 1) Mô tả đề / input

- File `flag_input.txt`:
  - Dòng 1: `n` (kích thước “brush”, ở đây `n = 60`).
  - Các dòng sau: mỗi dòng là một dãy các `k` (1-indexed). Với mỗi `k` ta in ra **chuỗi dài n** ký tự (mặc định là space `' '`) và đặt `'#'` tại các bit 1 của số trả về, theo thứ tự **MSB → LSB**.
- File `hint_input (1).txt` tương tự nhưng `n = 8` để hình nhỏ, là hint.

Kết quả của từng dòng là ghép các "khung n-bit" cạnh nhau để tạo nên một banner ASCII lớn (chứa hint / flag).

---

## 2) Đọc mã decompile (Hex-Rays) – ta cần gì?

Trong file decompile `chal (1).c`:

- Chương trình đọc `n` (gọi là _brush size_), kiểm tra `1 ≤ n ≤ 60`, đặt `M = (1<<n) - 1`.
- Với mỗi số `k` đọc được:
  1. Gọi một hàm (trong decompile là `sub_26DC`) để **tìm phần tử thứ k** của trình tự greedy “farthest-from-seen”.
  2. Gọi `sub_288B` để **render** số đó thành chuỗi dài `n` gồm `' '` và `'#'` (bit 1 → `'#'`).
- Sau khi xử lý hết chuỗi `k` của một dòng, in newline, tạo thành dòng ASCII.

Điểm mấu chốt: Nếu cài đặt naïve, `sub_26DC` sẽ mô phỏng (giữ BST/tập các điểm đã chọn, tìm khoảng xa nhất, …). Ta **không cần** làm thế – có công thức O(1) trực tiếp cho `k`.

---

## 3) Bản chất thuật toán – “chẻ đôi khoảng dài nhất” = midpoints dyadic

Quy trình:

1. Ban đầu có 2 đầu mút: `1` và `2^n-1`.
2. Luôn chọn số mới **có khoảng cách tối thiểu đến tập đã chọn là lớn nhất**. Điều này tương đương:
   - Luôn chọn **trung điểm** của khoảng trống dài nhất hiện tại.
   - Khi có nhiều khoảng cùng độ dài, thứ tự ổn định là theo cấp (tầng) chẻ đôi.

Hệ quả:

- Sau 2 phần tử đầu (endpoints), ta lần lượt chọn các **trung điểm dyadic** theo từng "tầng chẻ":
  **Tầng t = 0** (xa nhất): 1 điểm tại khoảng \([1,2^n-1]\) → `2^{n-1}`.
  **Tầng t = 1**: 2 điểm `1·2^{n-2}, 3·2^{n-2}`.
  **Tầng t = 2**: 4 điểm `1,3,5,7` nhân `2^{n-3}`.
  … cho tới **t = n-2**: có `2^{n-2}` điểm dạng `(2i+1)·2` (odd×2).
  Cuối cùng, **tầng cuối (distance = 0)** là các số lẻ còn lại `3,5,7,…,2^n-3` (trừ 2 endpoint).

Số lượng phần tử theo “khoảng cách” (hay theo tầng) vì vậy là:
`1, 2, 4, …, 2^{n-2}, 2^{n-1}-2`.

### Công thức O(1) cho phần tử thứ k

Đặt `M = 2^n - 1`.

- `k = 1` → `1`
- `k = 2` → `M`
- Với `r = k - 2` (bỏ qua 2 endpoint):
  - `t = floor(log2(r))` là tầng (tính từ 0).
  - Nếu `t < n-1`: phần tử thuộc một tầng chẻ đôi **không phải** tầng cuối.
    - `idx = r - 2^t` nằm trong `0..(2^t-1)` của tầng đó.
    - **Giá trị**: `((2*idx + 1) << (n-1 - t))`.
  - Ngược lại (`t ≥ n-1`): rơi vào **tầng cuối** (distance=0 – các số lẻ còn lại):
    - `idx = r - 2^(n-1)` trong `0..(2^(n-1)-3)`
    - **Giá trị**: `2*(idx + 1) + 1` (tức `3,5,7,…,2^n-3`).

> Trực giác: các tầng sinh theo dãy 1,2,4,… nên chỉ cần nhìn `bit_length` của `r` là biết ngay `t`.

### Độ phức tạp

- Mỗi truy vấn `k` chỉ tốn vài phép bit: **O(1)**.
- So với mô phỏng greedy (O(n log n) trở lên nếu dùng cấu trúc dữ liệu), tốc độ tăng rất lớn khi `n ≤ 60` nhưng có nhiều `k`.

---

## 4) Trích xuất ASCII và flag

- Render `hint_input` (n=8) sẽ cho một ảnh nhỏ – dùng để xác nhận mình render đúng chiều/đúng bit.
- Render `flag_input` (n=60) → ảnh banner lớn chứa **flag**.

Trong phần “Solve script” dưới đây, mình xuất luôn PNG cỡ lớn để đọc rõ, đồng thời lưu cả bản text (mỗi dòng là chuỗi `' '`/`'#'`) nếu thích mở bằng editor mono.

> Ảnh đã render sẵn từ inputs bạn cung cấp:
>
> - Hint: `sandbox:/mnt/data/hint_render.png`
> - Flag: `sandbox:/mnt/data/flag_render.png`

_Mở ảnh flag để đọc chuỗi flag (thường ở định dạng kiểu `CTF{...}` hoặc tương tự)._

---

## 5) Solve script (Python)

Script này:

1. Cài hàm `kth_value(n,k)` theo công thức trên.
2. Parse file input (`n`, các dãy `k`).
3. Render thành các dòng ASCII, vừa in ra `.txt`, vừa lưu `.png` phóng to để dễ đọc.

```python
#!/usr/bin/env python3
from pathlib import Path
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

# =============== core ===============
def kth_value(n: int, k: int) -> int:
    """Trả về giá trị ở vị trí k (1-indexed) của trình tự greedy-farthest
    trên [1, 2^n-1] với 2 endpoint đã có sẵn."""
    M = (1 << n) - 1
    if k == 1:
        return 1
    if k == 2:
        return M
    r = k - 2
    t = r.bit_length() - 1  # floor(log2(r))
    if t < n - 1:
        idx = r - (1 << t)
        return ( (2*idx + 1) << (n - 1 - t) )
    else:
        idx = r - (1 << (n - 1))  # 0..(2^(n-1)-3)
        return 2*(idx + 1) + 1

def render_ascii(n: int, rows: List[List[int]]) -> List[str]:
    lines = []
    for ks in rows:
        parts = []
        for k in ks:
            v = kth_value(n, k)
            s = [' '] * n
            for i in range(n-1, -1, -1):  # MSB -> LSB
                if (v >> i) & 1:
                    s[n - i - 1] = '#'
            parts.append(''.join(s))
        lines.append(''.join(parts))
    return lines

# =============== io helpers ===============
def parse_input(path: Path) -> Tuple[int, List[List[int]]]:
    text = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    n = int(text[0].strip())
    rows: List[List[int]] = []
    for line in text[1:]:
        if not line.strip():
            rows.append([])
        else:
            rows.append([int(x) for x in line.split()])
    return n, rows

def ascii_to_png(lines: List[str], out_png: Path, scale: int = 6):
    h = len(lines)
    w = max((len(l) for l in lines), default=0)
    arr = np.zeros((h, w), dtype=np.uint8)
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == '#':
                arr[y, x] = 1
    big = np.kron(arr, np.ones((scale, scale), dtype=np.uint8))
    plt.figure(figsize=(big.shape[1]/50, big.shape[0]/50))
    plt.imshow(big, cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(out_png, bbox_inches='tight', pad_inches=0)
    plt.close()

def write_txt(lines: List[str], out_txt: Path):
    out_txt.write_text('\n'.join(lines), encoding='utf-8')

# =============== main ===============
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('infile', type=Path, help='Đường dẫn input .txt (n; rồi các dãy k)')
    ap.add_argument('--png', type=Path, default=None, help='Xuất ảnh PNG phóng to để đọc')
    ap.add_argument('--txt', type=Path, default=None, help='Lưu bản text ASCII')
    ap.add_argument('--scale', type=int, default=6, help='Hệ số phóng to PNG (mặc định 6)')
    args = ap.parse_args()

    n, rows = parse_input(args.infile)
    lines = render_ascii(n, rows)

    if args.txt:
        write_txt(lines, args.txt)
        print(f"[+] Saved ASCII to {args.txt}")

    if args.png:
        ascii_to_png(lines, args.png, scale=args.scale)
        print(f"[+] Saved PNG to {args.png}")

    # Optional: in ra vài dòng để sanity-check
    for i, line in enumerate(lines[:3], 1):
        print(f"LINE {i:02d} |" + line[:120] + ("…" if len(line) > 120 else "") )
```

### Cách chạy

```bash
# Hint
python3 solve.py "hint_input (1).txt" --png hint.png --txt hint.txt --scale 10

# Flag
python3 solve.py flag_input.txt --png flag.png --txt flag.txt --scale 6
```

Mở `flag.png` để đọc flag.

```
FortID{Sk1bidy_Toil3t_Y0u_S0lv3d_7h3_Ur1n4l_S3lec710n_Pr0bl3m!}

```

## ![alt text](image-1.png)

![alt text](image.png)
