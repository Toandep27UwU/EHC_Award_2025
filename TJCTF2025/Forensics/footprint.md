![image](https://github.com/user-attachments/assets/8954402a-49ee-41e7-809b-974208b588cd)
đầu tiên mình dùng zipinfo để check một vài thông tin trong file zip, và mình thấy một file là .DS_Store
![image](https://github.com/user-attachments/assets/a5a1a41c-9275-440b-be11-1f3bfe833b2a)
nhưng khi giải nén nó ra mình lại k thấy nó, có thể nó đã bị ẩn hoặc có kí tự đặc biệt nên nó bị ẩn đi vầ khi dùng ls -a thì mình thấy lại file đó

(.DS_Store (viết tắt của Desktop Services Store) là một file ẩn do macOS tự động tạo ra trong các thư mục để lưu thông tin hiển thị trong Finder)
và khả năng trong files này sẽ có những file bị ẩn đi hoặc bị xóa thì mình có thể dùng 
"python -m ds_store .DS_Store" để kiểm tra nó và ra được output như dưới đây.
![image](https://github.com/user-attachments/assets/dd592738-055c-4908-b7b5-b64959c21cb1)

mình thấy các filename khá giống đnag bị encode thì mình đã dùng script decode.py đẻ decode các filename và trong một số filename chứa flag của chall này
![image](https://github.com/user-attachments/assets/d35ce864-1e25-4528-9ebb-b5076837788c)


 và ghép lại ta được flag là : tjctf{ds_store_is_useful?}
