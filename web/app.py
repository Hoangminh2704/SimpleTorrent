from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import split_file
from peer import download_from_metadata
app = Flask(__name__)
PIECES_DIR = "/Users/admin/Documents/241/MMT/MMT/files/pieces"
UPLOAD_DIR = "/Users/admin/Documents/241/MMT/MMT/files/uploads"
FILES_DIR = "/Users/admin/Documents/241/MMT/MMT/files"
# Tạo thư mục nếu chưa tồn tại
os.makedirs(PIECES_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
def list_metadata_files():
    return [f for f in os.listdir(FILES_DIR) if f.endswith("_metadata.json")]

@app.route('/')
def index():
    metadata_files = list_metadata_files()
    pieces = sorted(os.listdir(os.path.join(FILES_DIR, 'pieces')))
    return render_template('index.html', metadata_files=metadata_files, pieces=pieces)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(file_path)
        split_file(file_path)
        return redirect(url_for('index'))

@app.route('/download/<piece_name>')
def download(piece_name):
    piece_path = os.path.join(PIECES_DIR, piece_name)
    if os.path.exists(piece_path):
        return send_file(piece_path, as_attachment=True)
    else:
        return "Piece not found", 404

from utils import merge_pieces

@app.route('/select_metadata', methods=['POST'])
def select_metadata():
    metadata_file = request.form['metadata_file']
    video_name = metadata_file.replace("_metadata.json", "")
    merged_video_path = merge_pieces(video_name)

    if merged_video_path and os.path.exists(merged_video_path):
        return send_file(merged_video_path, as_attachment=True)
    else:
        return "Lỗi: Không thể hợp nhất video.", 500
# import os

# @app.route('/select_metadata', methods=['POST'])
# def select_metadata():
#     metadata_file = request.form['metadata_file']
#     video_name = metadata_file.replace("_metadata.json", "")
#     merged_video_path = os.path.abspath(f"files/{video_name}_reconstructed.mp4")

#     if merged_video_path and os.path.exists(merged_video_path):
#         return send_file(merged_video_path, as_attachment=True)
#     else:
#         return "Lỗi: Không thể tìm thấy video đã hợp nhất.", 404

# @app.route('/node_status')
# def node_status():
#     return node_states  # Trả về trạng thái của tất cả các node (giả sử node_states từ tracker)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
