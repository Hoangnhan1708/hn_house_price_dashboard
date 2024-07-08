import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import thư viện CORS

import pandas as pd
import google.generativeai as genai
# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:5501"}})




genai.configure(api_key="AIzaSyCA_8u5iEvnWpHFJtD5WdejRZggqTdvY5s")
os.environ['GOOGLE_API_KEY'] = "AIzaSyCA_8u5iEvnWpHFJtD5WdejRZggqTdvY5s"


# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)


df = pd.read_csv('../../datasets/processed/VN_housing_dataset_preprocessed.csv')


num_col_info_df = None

num_col_info_df = df.select_dtypes(include=np.number).copy()

def missing_ratio(column):
    return ((column.isnull().sum() / column.shape[0]) * 100).round(1)

def lower_quartile(column):
    return (column.quantile(0.25)).round(1)

def median(column):
    return (column.median())

def upper_quartile(column):
    return (column.quantile(0.75)).round(1)

# Làm tròn giá trị đến 1 chữ số thập phân
num_col_info_df = num_col_info_df.round(1)

num_col_info_df = num_col_info_df.agg([missing_ratio, "min", lower_quartile, median, upper_quartile, "max"])

cat_col_info_df = df.select_dtypes(exclude=[np.number])

def missing_ratio(column):
    return ((column.isnull().sum() / column.shape[0]) * 100).round(1)

# Hàm tính số lượng giá trị
def num_values(column):
    return column.nunique()

# Hàm tính tỷ lệ của từng giá trị
def value_ratios(column):
    value_counts = column.value_counts() #Đếm số lượng của mỗi loại value trong 1 cột
    non_missing_count = value_counts.sum() #Tổng số lượng của tất cả value trong 1 cột
    ratios = (value_counts / non_missing_count * 100).round(1) #Lưu tỉ lệ vào Series
    ratios_dict = ratios.to_dict()
    sorted_ratios_dict = dict(sorted(ratios_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_ratios_dict

cat_col_info_df = cat_col_info_df.agg([missing_ratio, num_values, value_ratios])



desc = str(df.describe().to_dict())
cols = str(df.columns.to_list())
dtype = str(df.dtypes.to_dict())
num_col_info_dict = str(num_col_info_df.to_dict())
cat_col_info_dict = str(cat_col_info_df.to_dict())


knowledge = [cat_col_info_dict, num_col_info_dict, desc, cols,dtype]

history_full = [
    {
        "role": "user",
        "parts": knowledge
    }
]


@app.route('/query', methods=['POST'])
def query():
    # Lấy dữ liệu từ body của yêu cầu POST
    content = request.json.get('content', '')  # Lấy nội dung từ body yêu cầu POST
    
    # Thực hiện gọi tới Gemini API
    try:
        
        chat_session = model.start_chat(
        history= history_full
        )
        # Thêm câu hỏi vào lịch sử
        history_full.append({
            "role": "user",
            "parts": content
        })
        
        response = chat_session.send_message(content)
         # Thêm câu trả lời vào lịch sử
        history_full.append({
            "role": "model",
            "parts": response.text
        })
        

        return jsonify({'content': response.text})

    except Exception as e:
        print('Error calling Gemini API:', e)
        return jsonify({'error': 'Failed to get response from Gemini API'}), 500

# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True, port=3000)
    
    
