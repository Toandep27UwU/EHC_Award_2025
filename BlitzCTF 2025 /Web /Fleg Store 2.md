![image](https://github.com/user-attachments/assets/7ae58f4b-5c69-4a68-aafe-2f0ce31606fa)![image](https://github.com/user-attachments/assets/1c02b03f-634b-458c-b818-6f4e8b50981f)

# ANALYZE

![image](https://github.com/user-attachments/assets/82d46c13-71e9-4d82-b06e-336221504da0)

nhìn qua thì đây là 1 trang web tính điểm bằng cách click , và đã bị giới hạn số lượng click là khoảng 1 click /s

và flag có giá 99.999 nếu làm như vậy thì tới tết tây chưa xong .

Tiếp theo t chú ý đến tính năng backup dữ liệu , khi chúng ta bấm backup dữ liệu thì ta sẽ tải về được file Json chứa số lượng click của bản thân.

Và tính năng tiếp theo chính là upload file json để backup lại dữ liệu cũ.

ý tưởng ở đây chính là giả mạo file Json để cho nó có sẵn luôn 10.000 điểm click

 # EXPLOIT

 ở đây ta sẽ tiến hành sửa 1 số dữ liệu trong file json 

 Đầu tiên ta sẽ sửa lại số lượng click được lưu trữ

 ```
  "session_data": {
    "timestamp": "2025-07-06T11:49:39.770675",
    "clicks_data": {
      "clickStore": 10000,
      "currency": "tokens",
      "daily_limit_reached": false
    },
```

Tiếp theo là về vấn đề bảo mật và lưu trữ trong file json

Tôi sẽ tiến hành xóa 2 key là `integrity_check` và `previous_backup_hash`

```
 "security": {
    "session_token": "3b4565c97d643ad59293622e8eddac85",
    "csrf_token": "d3368dfccb99deab641f2bdd49ebb06682ec2f09325560d29a11543f850acd0c",
    "integrity_check": "df1b9e99f55de54c14443c51b09ef4bbc63c75d1f7555a3831d97a09b4a8ba4d900d12551172a3f46245c31794a0a41214ed1e0cf59d107e8f515ce5db81dfdb",
    "previous_backup_hash": "3b9e69a6beae74069f74d3b2f94668d4a0249d1f"
  },
```

trở thành :

```
  "security": {
    "session_token": "3b4565c97d643ad59293622e8eddac85",
    "csrf_token": "d3368dfccb99deab641f2bdd49ebb06682ec2f09325560d29a11543f850acd0c"
  },
```

Và bây giờ chúng ta sẽ tiến hành upload nó lên lại

![image](https://github.com/user-attachments/assets/b42dae22-c9ec-4249-a0a8-8ab4c45bf647)

![image](https://github.com/user-attachments/assets/7c080e24-b6c4-4a50-9c75-ab590c504e0e)

# FLAG

```
Blitz{FlEg_l00t3R_sh0p_Butt_w1th_cl1qu35}
```
