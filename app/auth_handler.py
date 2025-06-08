import json
import logging
import user_manager as um
import connection_manager as cm

async def handle_register(websocket, data):
    """Xử lý yêu cầu đăng ký."""
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        await websocket.send(json.dumps({"type": "auth_response", "status": "error", "message": "Tên đăng nhập và mật khẩu không được để trống."}))
        return

    if username in um.users:
        await websocket.send(json.dumps({"type": "auth_response", "status": "error", "message": "Tên đăng nhập đã tồn tại."}))
        return
    
    # Thêm user mới vào database
    um.users[username] = {
        "passwordHash": um.hash_password(password),
        "avatarColor": um.generate_avatar_color()
    }
    um.save_users() # Lưu lại file
    logging.info(f"Người dùng mới đã đăng ký: {username}")
    await websocket.send(json.dumps({"type": "auth_response", "status": "success", "message": "Đăng ký thành công! Vui lòng đăng nhập."}))

async def handle_login(websocket, data):
    """Xử lý yêu cầu đăng nhập."""
    username = data.get("username")
    password = data.get("password")

    user_data = um.users.get(username)
    # Kiểm tra user và mật khẩu đã mã hóa
    if user_data and user_data["passwordHash"] == um.hash_password(password):
        cm.add_user(username, websocket) # Thêm vào danh sách online
        
        logging.info(f"Người dùng '{username}' đã đăng nhập từ {websocket.remote_address}")
        # Gửi thông tin user về cho client
        await websocket.send(json.dumps({
            "type": "auth_response", 
            "status": "success", 
            "message": "Đăng nhập thành công!", 
            "userData": {"username": username, "avatarColor": user_data["avatarColor"]}
        }))
        await cm.broadcast_user_list() # Cập nhật danh sách online cho mọi người
    else:
        await websocket.send(json.dumps({"type": "auth_response", "status": "error", "message": "Tên đăng nhập hoặc mật khẩu không chính xác."}))
