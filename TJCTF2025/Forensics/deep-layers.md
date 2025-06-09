![Image](https://github.com/user-attachments/assets/63ba32cc-0202-4205-916a-ca5fb561222a)

![chall](https://github.com/user-attachments/assets/091ca6b8-fb84-4195-90f7-000a5789972b)

đầu tiên mình dùng exiftool thì có tìm được một đoạn base64 và một thông tin là :
Warning                         : [minor] Trailer data after PNG IEND chunk

![image](https://github.com/user-attachments/assets/c17914c8-516b-4952-8ddc-271c9860ce0b)

sau đó mình đã check hex của ảnh này trên HxD và thấy được nó đang có file chèn bên trong đó.
mình dùng binwalk kiểm tra và biết đc nó bị chèn thêm file zip
![image](https://github.com/user-attachments/assets/45a093ff-fdd1-48fa-b227-0acefbc1c9ad)

sau đó mình dùng binwalk -e chall.png để lấy ra file zip.
file này sẽ yêu cầu password (pass chính là base64 được decode mình đã thấy khi dùng exiftool)
![image](https://github.com/user-attachments/assets/f6ec8306-4115-47aa-8906-a7ecffaf5dd1)
và mình chỉ cần giải nén nó và lấy flag
![image](https://github.com/user-attachments/assets/01eb35f8-ce2a-4b37-aac6-1e60edddc2b0)

Flags : tjctf{p0lygl0t_r3bb1t_h0l3}
