
# import socket
# import threading
# import os
# import json

# # Lưu thông tin về các phần file và trạng thái của node
# pieces_info = {}  # {piece: [{'node': 'node_address', 'status': 'started/stopped/completed'}]}
# node_states = {}  # {node: 'started/stopped/completed'}

# # Đăng ký thông tin các phần file với tracker
# def register_with_tracker(pieces, node):
#     for piece in pieces:
#         if piece not in pieces_info:
#             pieces_info[piece] = []
#         pieces_info[piece].append({'node': node, 'status': 'started'})
#     node_states[node] = 'started'

# # Cập nhật trạng thái node
# def update_node_state(node, state):
#     if state in ['started', 'stopped', 'completed']:
#         node_states[node] = state
#         # Cập nhật trạng thái cho các phần file của node
#         for piece, nodes in pieces_info.items():
#             for entry in nodes:
#                 if entry['node'] == node:
#                     entry['status'] = state

# # Xử lý các yêu cầu từ client (peer)
# def handle_client(conn, addr):
#     request = conn.recv(1024).decode()

#     # Đăng ký thông tin các phần file
#     if request.startswith("REGISTER"):
#         node, pieces = request.split(":")[1], request.split(":")[2].split(",")
#         register_with_tracker(pieces, node)
#         conn.send("Registered successfully".encode())

#     # Cập nhật trạng thái node
#     elif request.startswith("STATE"):
#         node, state = request.split(":")[1], request.split(":")[2]
#         if state in ['started', 'stopped', 'completed']:
#             update_node_state(node, state)
#             conn.send(f"Node state updated to {state}".encode())
#         else:
#             conn.send("Invalid state".encode())

#     # Yêu cầu tải phần file
#     elif request.startswith("REQUEST"):
#         piece = request.split(":")[1]
#         # Lọc chỉ những nodes có trạng thái "started"
#         nodes = [entry['node'] for entry in pieces_info.get(piece, []) if entry['status'] == 'started']
#         conn.send(",".join(nodes).encode())

#     conn.close()

# # Khởi động server của tracker
# def start_tracker():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(("0.0.0.0", 8000))
#     server.listen(5)
#     print("Tracker Server đang chạy...")

#     while True:
#         conn, addr = server.accept()
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()

# if __name__ == "__main__":
#     start_tracker()
# import socket
# import threading
# import os
# import json
# import logging

# # Cấu hình logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# # Lưu thông tin về các phần file và trạng thái của node
# pieces_info = {}  # {piece: [{'node': 'node_address', 'status': 'started/stopped/completed'}]}
# node_states = {}  # {node: 'started/stopped/completed'}

# # Đăng ký thông tin các phần file với tracker
# def register_with_tracker(pieces, node):
#     logging.info(f"Đang đăng ký node {node} với các phần file: {', '.join(pieces)}")
#     for piece in pieces:
#         if piece not in pieces_info:
#             pieces_info[piece] = []
#         pieces_info[piece].append({'node': node, 'status': 'started'})
#     node_states[node] = 'started'
#     logging.info(f"Node {node} đã đăng ký thành công.")

# # Cập nhật trạng thái node
# def update_node_state(node, state):
#     logging.info(f"Cập nhật trạng thái node {node} thành {state}")
#     if state in ['started', 'stopped', 'completed']:
#         node_states[node] = state
#         # Cập nhật trạng thái cho các phần file của node
#         for piece, nodes in pieces_info.items():
#             for entry in nodes:
#                 if entry['node'] == node:
#                     entry['status'] = state
#         logging.info(f"Trạng thái node {node} và các phần file đã được cập nhật.")
#     else:
#         logging.warning(f"Trạng thái node {node} không hợp lệ: {state}")

# # Xử lý các yêu cầu từ client (peer)
# def handle_client(conn, addr):
#     request = conn.recv(1024).decode()
#     logging.info(f"Nhận yêu cầu từ {addr}: {request}")

#     # Đăng ký thông tin các phần file
#     if request.startswith("REGISTER"):
#         node, pieces = request.split(":")[1], request.split(":")[2].split(",")
#         register_with_tracker(pieces, node)
#         conn.send("Registered successfully".encode())

#     # Cập nhật trạng thái node
#     elif request.startswith("STATE"):
#         node, state = request.split(":")[1], request.split(":")[2]
#         if state in ['started', 'stopped', 'completed']:
#             update_node_state(node, state)
#             conn.send(f"Node state updated to {state}".encode())
#         else:
#             conn.send("Invalid state".encode())
#             logging.warning(f"Trạng thái node {state} không hợp lệ.")

#     # Yêu cầu tải phần file
#     elif request.startswith("REQUEST"):
#         piece = request.split(":")[1]
#         # Lọc chỉ những nodes có trạng thái "started"
#         nodes = [entry['node'] for entry in pieces_info.get(piece, []) if entry['status'] == 'started']
#         logging.info(f"Yêu cầu tải phần file {piece} từ peer, trả về các node: {', '.join(nodes)}")
#         conn.send(",".join(nodes).encode())

#     conn.close()
#     logging.info(f"Đã xử lý xong yêu cầu từ {addr}")

# # Khởi động server của tracker
# def start_tracker():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(("0.0.0.0", 8000))
#     server.listen(5)
#     logging.info("Tracker Server đang chạy...")

#     while True:
#         conn, addr = server.accept()
#         logging.info(f"Chấp nhận kết nối từ {addr}")
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()

# if __name__ == "__main__":
#     start_tracker()



import socket
import threading
import os
import json
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Lưu thông tin về các phần file và trạng thái của node
pieces_info = {}  # {piece: [{'node': 'node_address', 'status': 'started/stopped/completed'}]}
node_states = {}  # {node: 'started/stopped/completed'}

# Đăng ký thông tin các phần file với tracker
# Giả sử mỗi peer có một phần file khác nhau
def register_with_tracker(pieces, node):
    logging.info(f"Đang đăng ký node {node} với các phần file: {', '.join(pieces)}")
    for piece in pieces:
        if piece not in pieces_info:
            pieces_info[piece] = []
        pieces_info[piece].append({'node': node, 'status': 'started'})
    
    # In ra thông tin của pieces_info để kiểm tra
    # logging.info(f"Hiện tại tracker có các pieces sau: {json.dumps(pieces_info, indent=4)}")
    
    node_states[node] = 'started'
    logging.info(f"Node {node} đã đăng ký thành công với các phần file: {', '.join(pieces)}")



# Cập nhật trạng thái node
def update_node_state(node, state):
    logging.info(f"Cập nhật trạng thái node {node} thành {state}")
    if state in ['started', 'stopped', 'completed']:
        node_states[node] = state
        # Cập nhật trạng thái cho các phần file của node
        for piece, nodes in pieces_info.items():
            for entry in nodes:
                if entry['node'] == node:
                    entry['status'] = state
        logging.info(f"Trạng thái node {node} và các phần file đã được cập nhật.")
    else:
        logging.warning(f"Trạng thái node {node} không hợp lệ: {state}")

# Xử lý các yêu cầu từ client (peer)
def handle_client(conn, addr):
    request = conn.recv(1024).decode()
    logging.info(f"Nhận yêu cầu từ {addr}: {request}")

    # Đăng ký thông tin các phần file
    if request.startswith("REGISTER"):
        node, pieces = request.split(":")[1], request.split(":")[2].split(",")
        register_with_tracker(pieces, node)
        conn.send("Registered successfully".encode())

    # Cập nhật trạng thái node
    elif request.startswith("STATE"):
        node, state = request.split(":")[1], request.split(":")[2]
        if state in ['started', 'stopped', 'completed']:
            update_node_state(node, state)
            conn.send(f"Node state updated to {state}".encode())
        else:
            conn.send("Invalid state".encode())
            logging.warning(f"Trạng thái node {state} không hợp lệ.")

    # Yêu cầu tải phần file
    elif request.startswith("REQUEST"):
        piece = request.split(":")[1]
        logging.info(f"Peer yêu cầu phần file: {piece}")
        
        # Lọc chỉ những nodes có trạng thái "started"
        nodes = [entry['node'] for entry in pieces_info.get(piece, []) if entry['status'] == 'started']
        
        # Log các node có phần file yêu cầu
        if nodes:
            logging.info(f"Phần file {piece} có sẵn ở các node: {', '.join(nodes)}")
        else:
            logging.info(f"Không có node nào có phần file {piece}.")
        
        conn.send(",".join(nodes).encode())

    conn.close()
    logging.info(f"Đã xử lý xong yêu cầu từ {addr}")

# Khởi động server của tracker
def start_tracker():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8000))
    server.listen(5)
    logging.info("Tracker Server đang chạy...")

    while True:
        conn, addr = server.accept()
        logging.info(f"Chấp nhận kết nối từ {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_tracker()
