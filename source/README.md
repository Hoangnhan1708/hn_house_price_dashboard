# Hướng dẫn build và run chương trình
## 📌 Môi trường thực thi
### 1. IDE
Sử dụng Visual Studio Code
### 2. Ngôn ngữ lập trình
- **Client**:
    - HTML
    - CSS
    - Javascript
- **Server**:
    - Python, framework Flask
### 3. Thư viện/ framework
- **Client**:
    - **Bootstrap**: nhóm đã thêm bằng cdn (thêm bằng link)
- **Server**:
    - **Flask**: `pip install flask`
    - **Flask_cors**: `pip install flask-cors`
    - **numpy**: `pip install numpy`
    - **pandas**: `pip install pandas`
    - **google.generativeai**: `pip install google-generativeai`
### 4. Extension:
- Live server
## 📌 Các bước run chương trình
- Mở workspace folder trong Visual Studio Code
- **Client**:
    1. Ở mở file `index.html` sau đó ấn chuột phải và chọn `Open with live server`.
    2. Kiểm tra `PORT` đang chạy ở góc dưới cùng bên phải hoặc trên thanh URL của browser và ghi nhớ.
- **Server**:
    1. Sử dụng PORT đang được chạy ở Client để sửa vào dòng `CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:5500"}})` trong file `server.py`
    1. Ở góc trên cùng bên trái chọn `Terminal -> New Terminal`
    2. Gõ lệnh `cd source/server`
    3. Và chạy bằng lệnh `python server.py`