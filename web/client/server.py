import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import thư viện CORS
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app, resources={r"/query": {"origins": "http://127.0.0.1:5501"}})

csv_loader = CSVLoader(file_path = '../../VN_housing_dataset_preprocessed.csv', encoding = "utf-8", csv_args={
  'delimiter': ','
})
data = csv_loader.load()



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

# def get_model_response(file,query):
#   #Function to get response from GEMINI PRO def get_model_response(file, query):
# # Split the context text into manageable chunks
  
#   text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200) 
#   context = "\n\n".join(str(p.page_content) for p in file)
#   data = text_splitter.split_text(context)
  
#   embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") 
#   searcher = Chroma.from_texts (data, embeddings).as_retriever()
#   print("hihi")
#   q = "Which price is largest?"
#   records = searcher.get_relevant_documents(q) 
#   print (records)
#   prompt_template ="""
#     You have to answer the question from the provided context and make sure that you provide all the details\n 
#     Context: {context}?\n
#     Question: {question} \n
    
#     Answer:
#   """
  

#   prompt = PromptTemplate(template=prompt_template, input_variables= ["context", "question"])
#   model = ChatGoogleGenerativeAI (model="gemini-1.5-flash", temperature=0.9)
#   chain = load_qa_chain (model, chain_type="stuff", prompt= prompt)
#   response = chain (
#     {
#     "input_documents": records, "question": query
#     }
#    , return_only_outputs=True)
#   return response['output_text']
  

@app.route('/query', methods=['POST'])
def query():
    # Lấy dữ liệu từ body của yêu cầu POST
    content = request.json.get('content', '')  # Lấy nội dung từ body yêu cầu POST
    
    # Thực hiện gọi tới Gemini API
    try:
        
        chat_session = model.start_chat(
        history=[
        ]
        )
        
        response = chat_session.send_message(content)
        # response = get_model_response(data, content)
        
        # return jsonify({'content': response})
        return jsonify({'content': response.text})

    except Exception as e:
        print('Error calling Gemini API:', e)
        return jsonify({'error': 'Failed to get response from Gemini API'}), 500

# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True, port=3000)