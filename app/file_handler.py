import json
import logging
import connection_manager as cm

async def handle_send_file(websocket, data):
    """Xử lý yêu cầu gửi file."""
    sender_username = cm.get_username_by_websocket(websocket)
    if not sender_username:
        await websocket.send(json.dumps({"type": "error_response", "message": "Lỗi xác thực người gửi."}))
        return

    recipient_username = data.get("recipient")
    if not recipient_username:
        await websocket.send(json.dumps({"type": "error_response", "message": "Vui lòng chọn người nhận."}))
        return

    # Lấy websocket của người nhận từ connection_manager
    recipient_ws = cm.get_websocket_by_username(recipient_username)
    if not recipient_ws:
        await websocket.send(json.dumps({"type": "error_response", "message": f"Người dùng '{recipient_username}' không online hoặc không tồn tại."}))
        return

    # Tạo gói tin để chuyển tiếp
    file_payload = {
        "type": "receive_file",
        "sender": sender_username,
        "filename": data.get("filename"),
        "payload": data.get("payload"),
        "hash": data.get("hash")
    }
    await recipient_ws.send(json.dumps(file_payload))
    
    # Gửi xác nhận cho người gửi
    await websocket.send(json.dumps({"type": "transfer_response", "status": "success", "message": f"Đã gửi file thành công cho {recipient_username}."}))
    logging.info(f"'{sender_username}' đã gửi file '{data.get('filename')}' cho '{recipient_username}'")
