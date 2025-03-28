from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import path, include
from students.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  
    path('students/', include('students.urls')),  
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('chatbot.urls')),
    path('api/students/', include('students.urls')),
    path('api/teachers/', include('teachers.urls')),
    # Thêm route để phục vụ media
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Phục vụ media và static khi DEBUG = True
if settings.DEBUG:
    print("Serving media at:", settings.MEDIA_URL, "from:", settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)