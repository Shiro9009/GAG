from django.contrib import admin
from django.urls import path, include
from .views import page1, page2, page3, page4, page5

urlpatterns = [
        path('', page1),
        path('2', page2),
        path('3', page3),
        path('4', page4),
        path('5', page5),
]
