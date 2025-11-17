from django.contrib import admin
from django.urls import path, include
from .views import page1, page2, page3, page4, page5, page6, page7
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', page1, name='home'),
    path('profile/', page2, name='profile'),
    path('stream/', page3, name='stream_current'),
    path('stream/<int:stream_id>/', page3, name='stream_detail'),
    path('user/<int:user_id>/', page4, name='user_profile'),
    path('categories/', page5, name='categories'),
    path('login/', page6, name='login'),
    path('regist/', page7, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)