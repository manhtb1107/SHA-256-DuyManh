import asyncio
import json
import logging
# Import user_manager để có thể truy cập thông tin người dùng (vd: màu avatar)
import user_manager as um

# Dictionary để theo dõi những người dùng đang online
# Cấu trúc: { "tên_người_dùng": đối_tượng_websocket }
connected_clients = {}

async def broadcast_user_list():
    """Gửi danh sách tất cả người dùng đang online tới mọi client."""
    if not connected_clients:
        return
    
    # Tạo danh sách người dùng online kèm thông tin cần thiết
    online_users_data = [
        {
            "username": username,
            "avatarColor": um.users.get(username, {}).get("avatarColor", "#cccccc") # Lấy màu avatar, có giá trị mặc định
        } for username in connected_clients.keys()
    ]

    # Tạo gói tin để gửi đi
    broadcast_message = json.dumps({
        "type": "user_list_update",
        "users": online_users_data
    })
    
    # SỬA LỖI: Thay thế asyncio.wait bằng asyncio.gather
    # asyncio.gather là cách hiện đại và được khuyến nghị để chạy các coroutine đồng thời.
    if connected_clients:
        tasks = [client.send(broadcast_message) for client in connected_clients.values()]
        await asyncio.gather(*tasks)
        
    logging.info(f"Đã broadcast danh sách online: {list(connected_clients.keys())}")

def add_user(username, websocket):
    """Thêm một người dùng vào danh sách online khi họ đăng nhập."""
    connected_clients[username] = websocket

def remove_user(websocket):
    """Xóa một người dùng khỏi danh sách online khi họ ngắt kết nối."""
    username_disconnected = next((user for user, ws in connected_clients.items() if ws == websocket), None)
    if username_disconnected:
        del connected_clients[username_disconnected]
        logging.info(f"Người dùng '{username_disconnected}' đã đăng xuất.")
        return True # Trả về True nếu có người dùng bị xóa
    return False

def get_websocket_by_username(username):
    """Lấy đối tượng websocket của một người dùng dựa trên tên."""
    return connected_clients.get(username)

def get_username_by_websocket(websocket):
    """Lấy tên người dùng từ đối tượng websocket."""
    return next((user for user, ws in connected_clients.items() if ws == websocket), None)
