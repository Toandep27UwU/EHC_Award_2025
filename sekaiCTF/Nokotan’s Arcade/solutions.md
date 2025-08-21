__Tóm tắt__

khu trò chơi mở cửa __n__ phút, __m__ người chơi i trong khoảng  __[li,ri]__ và một ván dài __t__ phút
mỗi ván người chơi i hoàn thành nhận được __pi__ giá trị 

==> Hỏi tổng điểm phổ biến tối đa có thể thu được


__Hướng giải__

Gọi T = n - t + 1 là số thời điểm bắt đầu hợp lệ tối đa (s = 1..T)
(Ván bắt đầu ở s chiếm s..s+t-1, cần s+t-1 ≤ n => s ≤ n - t + 1)

Với mỗi s, định nghĩa gain[s] = điểm tốt nhất nếu mở ván bắt đầu tại s (tức max của các p đang phủ s).


với mỗi người (l,r,p):
Họ phủ đoạn thời điểm bắt đầu s ∈ [l, r - t + 1]
Ta không lặp cả đoạn; thay vào đó tạo 2 sự kiện:
add[l] → p bắt đầu hiệu lực tại s = l
remove[r - t + 2] --> từ s = r - t + 2 trở đi không còn hiệu lực (nên vẫn hiệu lực tới hết s = r - t + 1)

__Tiếp theo__

Ta cần lấy max p đang hiệu lực ở mỗi s. Thay vì multiset, code dùng
active (max-heap): chứa các p đang hiệu lực
trash (max-heap): chứa các p vừa hết hiệu lực (để xoá lười)
__Tại mỗi s:__
Đẩy mọi p trong add[s] vào active
Đẩy mọi p trong remove[s] vào trash (đánh dấu sắp xoá)
Gột trash: trong khi đỉnh 2 heap bằng nhau, pop cả hai --> tương đương xoá đúng một bản sao p
gain[s] = đỉnh của active (nếu rỗng thì 0)

Đặt dp[i] = điểm tối đa trong i phút đầu ([1..i]):
Mặc định: không kết thúc ván ở i --> dp[i] = dp[i-1]
Nếu i ≥ t: có thể có một ván kết thúc ở i, bắt đầu tại i - t + 1

`dp[i] = max(dp[i],
            dp[i - t] + gain[i - t + 1])`

Kết quả là dp[n]
Ván dài t kết thúc ở i thì bắt đầu ở i - t + 1. Lợi ích ván đó là gain tại thời điểm bắt đầu nên ta có chỉ số i - t + 1


Sweep line đảm bảo tại mọi s ta biết đúng tập người còn hiệu lực; lấy max p là tối ưu nếu chọn mở ván ở s
DP độ dài cố định: nếu mở ván kết thúc ở i, phần trước i - t độc lập (không chồng). Hai lựa chọn ở mỗi i (mở/không mở) bao trùm mọi phương án --> lấy max

__Về độ phức tạp :__

Tạo sự kiện: O(m)
Mỗi p được thêm 1 lần vào active và 1 lần vào trash; mỗi thao tác heap O(log m) → sweep O((T + m) log m) với T ≤ n
DP : O(n)
Bộ nhớ : O(n+m) trên thực tế là O(n + valid)

__Các điều cần đảm bảo trong code : 
Nếu t > n → in 0 và dừng
Với mỗi (l, r, p), chỉ tạo event khi l ≤ r - t + 1
remove đặt tại end + 1 để p còn hiệu lực đến hết end
Hai heap active/trash: luôn gột rác trước khi đọc top
DP đúng công thức dp[i] = max(dp[i-1], dp[i - t] + gain[i - t + 1])

