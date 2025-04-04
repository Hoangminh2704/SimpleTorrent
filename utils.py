import os
import hashlib

PIECES_DIR = "/Users/admin/Documents/241/MMT/MMT/files/pieces"

# Chia file thành các phần nhỏ


import json



def split_file(file_path, piece_size=512 * 1024):
    file_name = os.path.basename(file_path).split('.')[0]
    pieces_dir = PIECES_DIR
    os.makedirs(pieces_dir, exist_ok=True)

    metadata = []
    with open(file_path, "rb") as f:
        index = 1
        while chunk := f.read(piece_size):
            piece_name = f"{file_name}_piece_{index}"
            piece_path = os.path.join(pieces_dir, piece_name)

            # Lưu phần file mà không tính hash
            with open(piece_path, "wb") as piece_file:
                piece_file.write(chunk)

            # Lưu metadata với tên phần mà không có hash
            metadata.append({
                "piece_name": piece_name
            })
            index += 1

    # Lưu metadata vào file JSON
    metadata_path = f"/Users/admin/Documents/241/MMT/MMT/files/{file_name}_metadata.json"
    with open(metadata_path, "w") as meta_file:
        json.dump(metadata, meta_file, indent=4)
    print(f"File đã được chia thành các phần nhỏ và lưu metadata tại {metadata_path}.")






# Tạo hash cho một phần file
def hash_piece(piece_path):
    with open(piece_path, "rb") as f:
        data = f.read()
        return hashlib.sha1(data).hexdigest()


import os

def merge_pieces(video_name):
    print(f"Bắt đầu hợp nhất các phần file cho video: {video_name}")

    pieces_dir = "/Users/admin/Documents/241/MMT/MMT/files/pieces"  # Thư mục chứa các pieces
    list_file_path = f"/Users/admin/Documents/241/MMT/MMT/files/{video_name}_list.txt"

    # Tạo file danh sách các phần file
    with open(list_file_path, "w") as list_file:
        index = 1
        while True:
            piece_path = os.path.join(pieces_dir, f"{video_name}_piece_{index}")
            if not os.path.exists(piece_path):
                break
            list_file.write(f"file '{os.path.abspath(piece_path)}'\n")
            index += 1

    # Kiểm tra và tạo thư mục đích cho video hợp nhất
    output_dir = "/Users/admin/Documents/241/MMT/MMT/files/"
    os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

    merged_video_path = os.path.join(output_dir, f"{video_name}_reconstructed.mp4")
    merge_command = f"ffmpeg -f concat -safe 0 -i {list_file_path} -c copy {merged_video_path}"
    result = os.system(merge_command)

    if result == 0:
        print("Hợp nhất thành công!")
        return merged_video_path
    else:
        print("Lỗi khi hợp nhất file.")
        return None


