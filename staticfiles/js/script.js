function toggleDropdown() {
    var dropdownMenu = document.getElementById('dropdownMenu');
    dropdownMenu.classList.toggle('show');
}

// Đóng menu khi nhấp ra ngoài
window.onclick = function(event) {
    if (!event.target.matches('.btn-secondary')) {
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// Script cho Chatbot 

// Lấy CSRF token từ cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Hàm gửi tin nhắn
function sendMessage() {
    console.log('sendMessage function called'); // Log để kiểm tra hàm sendMessage có được gọi không
    var userMessage = document.getElementById('userMessage').value;
    if (userMessage.trim() !== '') {
        console.log('User message is not empty'); // Log để kiểm tra tin nhắn của người dùng
        var chatbox = document.getElementById('chatbox');
        var userMessageElement = document.createElement('div');
        userMessageElement.className = 'user-message';
        userMessageElement.innerText = userMessage;
        chatbox.appendChild(userMessageElement);
        document.getElementById('userMessage').value = '';

        fetch('/api/chat/', { // Sửa URL đúng với cấu hình của bạn
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response received from API'); // Log để kiểm tra phản hồi từ API
            var botMessageElement = document.createElement('div');
            botMessageElement.className = 'bot-message';
            botMessageElement.innerText = data.message;
            chatbox.appendChild(botMessageElement);
            chatbox.scrollTop = chatbox.scrollHeight;
        })
        .catch(error => {
            console.error('Lỗi:', error);
        });
    } else {
        console.log('User message is empty'); // Log để kiểm tra nếu tin nhắn người dùng rỗng
    }
}

// Thêm sự kiện click cho nút gửi
document.getElementById('sendButton').addEventListener('click', sendMessage);

// Thêm sự kiện nhấn phím Enter để gửi tin nhắn
document.getElementById('userMessage').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
