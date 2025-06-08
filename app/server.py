import asyncio
import websockets
import json
import logging
import sys

# --- THIẾT LẬP LOGGING ---
# Cấu hình logging để hiển thị thông tin chi tiết hơn
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    stream=sys.stdout # Đảm bảo log xuất ra console
)

logging.info("======================================================")
logging.info("=     KHỞI CHẠY FILE SERVER.PY (PHIÊN BẢN MỚI NHẤT)     =")
logging.info("======================================================")

# Import các module và handler đã được tách ra
try:
    import user_manager as um
    import connection_manager as cm
    from auth_handler import handle_login, handle_register
    from file_handler import handle_send_file
    logging.info("Tất cả các module đã được import thành công.")
except ImportError as e:
    logging.error(f"LỖI NGHIÊM TRỌNG: Không thể import module. Vui lòng kiểm tra các file .py. Chi tiết: {e}")
    # Thoát chương trình nếu không import được
    sys.exit(1)


# --- BỘ ĐIỀU KHIỂN CHÍNH ---
async def connection_handler(websocket):
    """Hàm xử lý chính, điều phối các hành động từ client."""
    # Nếu cần lấy địa chỉ client:
    remote_addr = getattr(websocket, "remote_address", None)
    logging.info(f"Client mới kết nối từ {remote_addr}")
    try:
        # Vòng lặp để lắng nghe tin nhắn từ client này
        async for message in websocket:
            logging.debug(f"Nhận tin nhắn thô: {message}")
            try:
                data = json.loads(message)
                action_type = data.get("type")
                logging.info(f"Đã nhận hành động '{action_type}' từ {websocket.remote_address}")

                # Điều phối hành động đến các handler tương ứng
                if action_type == "register":
                    await handle_register(websocket, data)
                elif action_type == "login":
                    await handle_login(websocket, data)
                elif action_type == "send_file":
                    await handle_send_file(websocket, data)
                else:
                    logging.warning(f"Nhận được hành động không rõ: {action_type}")
            
            except json.JSONDecodeError:
                logging.error("Lỗi giải mã tin nhắn JSON.")
            except Exception as e:
                logging.error(f"Đã xảy ra lỗi không mong muốn khi xử lý tin nhắn: {e}", exc_info=True)

    except websockets.exceptions.ConnectionClosed:
        logging.info(f"Client đã ngắt kết nối: {remote_addr}")
    finally:
        # Xử lý khi client ngắt kết nối
        if cm.remove_user(websocket):
            # Nếu có người dùng bị xóa, cập nhật danh sách online cho những người còn lại
            await cm.broadcast_user_list()

async def main():
    """Hàm chính để khởi chạy server WebSocket."""
    host = "localhost"
    port = 8765
    
    um.load_users() # Tải dữ liệu người dùng đã đăng ký khi bắt đầu
    
    logging.info(f"Server WebSocket chuẩn bị khởi chạy tại ws://{host}:{port}")
    try:
        # Không cần truyền path nữa
        async with websockets.serve(connection_handler, host, port, max_size=100_000_000):
            logging.info(">>> SERVER ĐÃ SẴN SÀNG NHẬN KẾT NỐI <<<")
            await asyncio.Future() # Chạy server mãi mãi
    except OSError as e:
        logging.error(f"LỖI KHỞI ĐỘNG SERVER: Không thể mở cổng {port}. Có thể một chương trình khác đang sử dụng cổng này. Chi tiết: {e}")
    except Exception as e:
        logging.error(f"LỖI KHỞI ĐỘNG SERVER KHÔNG XÁC ĐỊNH: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Xử lý khi người dùng nhấn Ctrl+C để dừng server
        logging.info("Đã nhận tín hiệu dừng server. Tạm biệt!")
