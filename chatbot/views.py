import spacy
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pathlib import Path

# Khởi tạo spaCy với mô hình ngôn ngữ
nlp = spacy.load("en_core_web_sm")

# Đường dẫn tới tệp JSON chứa dữ liệu câu hỏi và câu trả lời
FAQ_FILE = Path(__file__).resolve().parent / 'faq.json'

@api_view(['POST'])
def chatbot(request):
    user_message = request.data.get('message').strip()
    response_message = "Sorry, I didn't understand that. Can you please try again."

    if user_message:
        # Đọc dữ liệu câu hỏi và câu trả lời từ tệp JSON
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            faq_data = json.load(f)

        # Tìm câu trả lời cho câu hỏi người dùng
        response_message = faq_data.get(user_message, response_message)

    return Response({"message": response_message})
