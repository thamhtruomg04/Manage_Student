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
    user_message = request.data.get('message', '').strip()
    response_message = "Xin lỗi, tôi không hiểu. Bạn có thể thử lại không?"

    if user_message:
        try:
            with open(FAQ_FILE, 'r', encoding='utf-8') as f:
                faq_data = json.load(f)

            # Sử dụng spaCy để xử lý câu hỏi người dùng
            user_doc = nlp(user_message.lower())
            best_match = None
            best_similarity = 0.0

            # Tìm câu hỏi có độ tương đồng cao nhất
            for question in faq_data.keys():
                question_doc = nlp(question.lower())
                similarity = user_doc.similarity(question_doc)
                if similarity > best_similarity and similarity > 0.7:  # Ngưỡng tương đồng
                    best_similarity = similarity
                    best_match = question

            if best_match:
                response_message = faq_data[best_match]
        except FileNotFoundError:
            response_message = "Lỗi: Không tìm thấy tệp FAQ."
        except json.JSONDecodeError:
            response_message = "Lỗi: Định dạng dữ liệu FAQ không hợp lệ."
        except Exception as e:
            response_message = f"Lỗi: {str(e)}"

    return Response({"message": response_message})