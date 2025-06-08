Ứng dụng Gửi File Peer-to-Peer (P2P) An Toàn
Giới thiệu
Đây là một ứng dụng web cho phép người dùng gửi và nhận file trực tiếp với nhau (peer-to-peer) trong thời gian thực. Dự án được xây dựng với kiến trúc client-server sử dụng WebSocket để giao tiếp, trong đó server đóng vai trò trung gian để kết nối và điều phối, còn việc truyền tải file diễn ra trực tiếp giữa các client.

Điểm nổi bật của ứng dụng là tính năng kiểm tra toàn vẹn file bằng thuật toán băm SHA-256, đảm bảo file không bị thay đổi hoặc lỗi trong quá trình truyền.

Chức năng chính
Xác thực người dùng:

Hệ thống đăng ký và đăng nhập an toàn.

Mật khẩu người dùng được mã hóa bằng SHA-256 trước khi lưu trữ.

Danh sách người dùng Online:

Hiển thị danh sách những người dùng đang trực tuyến theo thời gian thực.

Mỗi người dùng có một avatar với màu sắc ngẫu nhiên để dễ nhận diện.

Gửi File trực tiếp (Peer-to-Peer):

Người dùng có thể chọn một người đang online từ danh sách để gửi file.

Giao diện kéo-thả (drag-and-drop) hiện đại và tiện lợi.

Kiểm tra toàn vẹn file (SHA-256):

Phía người gửi: Trước khi gửi, trình duyệt sẽ tự động tính toán mã hash SHA-256 của file.

Phía người nhận: Sau khi nhận được dữ liệu, trình duyệt sẽ tính toán lại mã hash và so sánh với mã hash gốc do người gửi cung cấp.

Giao diện sẽ hiển thị thông báo rõ ràng về kết quả xác thực:

Thành công: Nếu hai mã hash khớp nhau, file được xác nhận là toàn vẹn và tự động tải về.

Thất bại: Nếu mã hash không khớp, ứng dụng sẽ cảnh báo người dùng rằng file có thể đã bị lỗi hoặc bị can thiệp, nhưng vẫn cho phép tải về nếu muốn.

Thông báo Real-time:

Nhận thông báo tức thì khi có người dùng khác gửi file cho bạn.

Hiển thị tên file và mã hash SHA-256 của file được gửi đến.

Giao diện hiện đại & responsive:

Thiết kế gọn gàng, chuyên nghiệp với hiệu ứng "frosted glass".

Tương thích tốt trên nhiều kích thước màn hình.

Công nghệ sử dụng
Backend:

Ngôn ngữ: Python 3

Thư viện: websockets, asyncio để xử lý kết nối đồng thời hiệu năng cao.

Frontend:

HTML5, CSS3, JavaScript (ES6+)

Styling: Tailwind CSS cho việc xây dựng giao diện nhanh chóng và hiện đại.

Icons: Font Awesome.

Web APIs: WebSocket API, File API, Web Crypto API (cho việc tính toán SHA-256).

Giao thức: WebSocket (ws://)

Hướng dẫn cài đặt và chạy dự án
Clone repository:

git clone <URL_CUA_REPOSITORY>
cd <TEN_THU_MUC>

Cài đặt các thư viện Python cần thiết:

pip install websockets

Chạy Server:
Mở terminal và chạy lệnh sau:

python server.py

Server sẽ khởi động và lắng nghe kết nối tại ws://localhost:8765.

Mở ứng dụng trên trình duyệt:
Mở file index.html bằng trình duyệt web. Bạn có thể mở nhiều tab hoặc cửa sổ trình duyệt để giả lập nhiều người dùng khác nhau.

Sử dụng:

Đăng ký tài khoản mới trên một tab.

Đăng ký hoặc đăng nhập bằng tài khoản khác trên tab còn lại.

Bắt đầu gửi file và trải nghiệm!
