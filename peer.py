import socket
import threading
import os
from utils import hash_piece
import json

# Lấy địa chỉ tracker từ biến môi trường
TRACKER_HOST = os.getenv("TRACKER_HOST", "localhost")  # Tên dịch vụ hoặc địa chỉ IP của máy chạy tracker
TRACKER_PORT = int(os.getenv("TRACKER_PORT", 8001))  # Cổng 8000 cho tracker

def register_with_tracker(pieces):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to tracker at {TRACKER_HOST}:{TRACKER_PORT}")
        s.connect((TRACKER_HOST, TRACKER_PORT))  # Kết nối tới tracker qua cổng 8000
        message = f"REGISTER:Peer:{','.join(pieces)}"
        s.send(message.encode())
        response = s.recv(1024).decode()
        print(response)

# Tiếp tục các chức năng của peer, bao gồm tải xuống và chia sẻ video

PIECES_DIR = "files/pieces/"

# Yêu cầu tải một phần file từ tracker
def request_piece_from_tracker(piece):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        message = f"REQUEST:{piece}"
        s.send(message.encode())
        nodes = s.recv(1024).decode().split(",")
        return nodes
import requests
import hashlib

# import socket

# # Hàm để đăng ký các pieces mới với tracker
# def register_pieces_with_tracker(pieces):
#     tracker_host = "localhost"  # Hoặc tên của Docker container nếu sử dụng Docker
#     tracker_port = 8000  # Cổng tracker

#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((tracker_host, tracker_port))
#             message = f"REGISTER:Peer:{','.join(pieces)}"  # Gửi các pieces lên tracker
#             s.send(message.encode())
#             response = s.recv(1024).decode()
#             print(f"Phản hồi từ tracker: {response}")
#     except Exception as e:
#         print(f"Lỗi khi kết nối đến tracker: {e}")




def calculate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def download_piece(node, piece_name):
    try:
        print(f"Bắt đầu tải {piece_name} từ {node}...")
        host, port = node.split(":")
        url = f"http://{host}:{port}/download/{piece_name}"
        response = requests.get(url, stream=True, timeout=10)

        if response.status_code == 200:
            piece_path = os.path.join(PIECES_DIR, piece_name)
            with open(piece_path, "wb") as piece_file:
                for chunk in response.iter_content(chunk_size=8192):
                    piece_file.write(chunk)
            print(f"Tải thành công {piece_name}.")
        else:
            print(f"Lỗi khi tải {piece_name} từ {node}")
    except Exception as e:
        print(f"Exception khi tải {piece_name}: {e}")


# Tải một phần file từ node khác
# def download_piece(node, piece):
#     host, port = node.split(":")
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((host, int(port)))
#         s.send(piece.encode())
#         data = s.recv(1024)
#         piece_path = os.path.join(PIECES_DIR, piece)
#         with open(piece_path, "wb") as f:
#             f.write(data)
#         print(f"Downloaded {piece} from {node}")

# Upload phần file cho node khác
def handle_upload_request(conn):
    piece = conn.recv(1024).decode()
    piece_path = os.path.join(PIECES_DIR, piece)
    if os.path.exists(piece_path):
        with open(piece_path, "rb") as f:
            data = f.read()
            conn.send(data)
    conn.close()

# Khởi động server của peer
def start_peer_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9000))
    server.listen(5)
    print("Peer server đang chạy...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_upload_request, args=(conn,))
        thread.start()




def list_metadata_files():
    metadata_files = [f for f in os.listdir("files/") if f.endswith("_metadata.json")]
    return metadata_files

def download_from_metadata(node, metadata_file):
    with open(f"files/{metadata_file}", "r") as meta_file:
        metadata = json.load(meta_file)

    for piece_info in metadata:
        piece_name = piece_info["piece_name"]
        expected_hash = piece_info["hash"]
        download_piece(node, piece_name, expected_hash)

def update_state_with_tracker(state):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        message = f"STATE:Peer:{state}"
        s.send(message.encode())
        response = s.recv(1024).decode()
        print(response)



if __name__ == "__main__":
    # Lấy danh sách các phần file (pieces) thực tế trong thư mục files/pieces/
    pieces_dir = "files/pieces"
    pieces = [f for f in os.listdir(pieces_dir)]

    # Đảm bảo rằng danh sách pieces không rỗng
    if pieces:
        register_with_tracker(pieces)
        print(f"Đã đăng ký các phần file: {', '.join(pieces)}")
    else:
        print("Không tìm thấy các phần file (pieces) trong thư mục.")
    
    start_peer_server()
