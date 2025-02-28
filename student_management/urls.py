from django.contrib import admin
from django.urls import path, include
from students.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  
    path('students/', include('students.urls')),  
    path('api/', include('chatbot.urls')),
]
