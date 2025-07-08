![image](https://github.com/user-attachments/assets/a5f4c049-7839-493d-ba7c-08e2ce7dbc08)

[protected.zip](https://github.com/user-attachments/files/21118176/protected.zip)

khi mình mở file **protected.zip** để giải nén thì thấy có yêu cầu password để giải nén, mà trong bài k có cho password nên mình nghĩ có thể phải crack nó.
Nhưng khi mình đưa nó vào Hexeditor để đọc hex của file này thì thấy được password được giấu ở cuối file 

![image](https://github.com/user-attachments/assets/713f9832-4883-4e2d-9908-2b735cd5baea)

**passwd is iloveblitzhack**

và khi giải nén ra mình thấy được một file pcap và cùng mở nó lên nhé.

![image](https://github.com/user-attachments/assets/7c437e76-2ae5-4490-9aef-afc3df0e9c72)

![image](https://github.com/user-attachments/assets/6d0d78b4-fb66-4746-b957-afbd73c225eb)

ở đây mình thấy có 2 protocol là TCP và ICMP. Nhưng để ý từ packet đầu tiên, mình thấy data stegment có những data giống với một file png

![image](https://github.com/user-attachments/assets/0351a06c-c21d-4ff1-99ed-22b595d63f86)

và mình nghĩ các packet tcp này cũng là một ảnh png và được tách ra làm các packet đó, và khi mình kiểm tra packet tcp cuối cùng thì thấy được phần kết thúc của file PNG chính là **IEND**

![image](https://github.com/user-attachments/assets/e0ba4456-148d-49e4-b4a9-4f9b3595854e)


và mình dùng tshark để lấy payload của các packet này : **tshark -r blitzhack_traffic.pcap -Y "tcp" -T fields -e tcp.payload > payload.txt**

và sau đó mình dùng command : **tr -d ' \n' < payload.txt > decode.txt** để ghép nó lại rồi decode sang file png 

![image](https://github.com/user-attachments/assets/11546932-e685-4844-969c-d109236f4792)


![image](https://github.com/user-attachments/assets/0c0f64c0-e7b8-4dd3-98e4-33f9d9abb654)

 flag : Blitz{H3r3_1S_th3_flAG_G00d_B03}



