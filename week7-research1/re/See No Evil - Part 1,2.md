# See No Evil - Part 1 

<img width="1369" height="537" alt="image" src="https://github.com/user-attachments/assets/77a8dffa-0902-4db6-8358-154d5aeca765" />

Đây là file pe64 nên đưa vào ida để dịch ngược

<img width="721" height="524" alt="image" src="https://github.com/user-attachments/assets/2d766363-8da8-4f81-962e-0c54d0445e25" />

Vừa vào thì có giao diện như này, có vẻ bài này là 1 dạng anti debug vì nó thách thức debug:

<img width="1499" height="748" alt="image" src="https://github.com/user-attachments/assets/82142924-b024-4b83-8ae1-eb0332445a03" />

Đọc string trong có trong file thì có các level từ 1 đến 5, part 1 và 2 là level 1 và 2:

<img width="901" height="307" alt="image" src="https://github.com/user-attachments/assets/4f5bd68d-d579-4a5b-84fd-20d28aec2fee" />

Tôi đặt tạm cái breakpoint ở `0x7FF64192599D`:

<img width="1317" height="708" alt="image" src="https://github.com/user-attachments/assets/4a59312c-e5ce-4042-b78d-d5b95eccdaad" />

Nếu chạy sang bên trái thì nó out luôn vì nó antidebug, tôi chỉnh cho nó đi sang bên phải bằng flag zf

<img width="1474" height="862" alt="image" src="https://github.com/user-attachments/assets/86140696-e8d4-4a00-a82e-8bec9656c32c" />

Do bộ nhớ cấp phát ảo nên phải đặt breakpoint luôn chỗ in ra địa chỉ flag, nếu không là nó xóa thì không tìm thấy

<img width="498" height="714" alt="image" src="https://github.com/user-attachments/assets/2e2e76f2-1eaa-460b-9b1e-4091384b23bc" />

Copy địa chỉ đó và tới là ra flag

-----------------

# See No Evil - Part 2

<img width="1517" height="657" alt="image" src="https://github.com/user-attachments/assets/c3fa20ed-0637-40f5-ab54-eee71f908744" />

Tiếp theo là đoạn code của level 2:

<img width="875" height="632" alt="image" src="https://github.com/user-attachments/assets/57175cdc-ee1d-4ef5-859b-36d68f345d46" />

Đây là đoạn antidebug, phải né cái `cs:OutputDebugStringA` ra bằng cách đổi flag zf

<img width="966" height="783" alt="image" src="https://github.com/user-attachments/assets/b7cc6ea1-3cb9-416c-92df-2aa600899937" />

<img width="1565" height="774" alt="image" src="https://github.com/user-attachments/assets/d32e06d2-7dd9-49e3-9f2e-0e8d3fac5d45" />

Đi theo địa chỉ là ra flag

<img width="588" height="694" alt="image" src="https://github.com/user-attachments/assets/57b04183-9d9d-4f12-875e-59b4f65d23ac" />










