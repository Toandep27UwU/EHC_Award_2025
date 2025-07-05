# Tổng quan

![image](https://github.com/user-attachments/assets/b74f47f5-8369-4cf3-a71b-1421e8d3fecf)

Trang web này gồm có login và register, do chưa có tài khoản nên tôi đăng kí 1 cái:

![image](https://github.com/user-attachments/assets/bd41a79e-1402-458b-8ad5-77c2d36b3e1d)

Sau khi đăng kí thì vào được dashboard:

![image](https://github.com/user-attachments/assets/7c656dbe-80a8-4857-a3b1-371cab261b92)

Website gồm có dashboard, shop, cart, redeem, Generate Coupon và logout

Dashboard thì như hình, shop thì trong đó có flag để mua, cart thì là cái đã thêm giỏ hàng, redeem là thêm mã được lấy từ Generate Coupon

Tôi test thử thì tối đa được 50 trong khi giá để mua flag là 70

![image](https://github.com/user-attachments/assets/0c661441-9865-430c-9784-eaea515a5d8d)

# Giả thiết

Dựa vào cái hình thức này thì tôi đoán là race condition, tôi nghĩ nếu là race condition thì khi gửi 1 đống request, server sẽ hiểu nhầm là không biết cái mã này dùng chưa vì nó không kịp cập nhật tình trạng của mã

# Khai thác

Tôi làm hẳn 60 cái req trong burp và để ở chế độ gửi song song

![image](https://github.com/user-attachments/assets/39a036ce-f9c3-4e88-b11a-c571b1c01823)

Sau khi bấm gửi thì quay lại dashboard và f5 lại trang thì đã có 70, đủ để mua flag

![image](https://github.com/user-attachments/assets/2e780470-a2fd-402e-8bc9-b0c466721429)

Đã mua

![image](https://github.com/user-attachments/assets/ff599992-f795-47b1-ae25-8ba290ce5340)

Truy cập vào /flag.txt là tải file flag.txt về



