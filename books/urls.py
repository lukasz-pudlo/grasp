from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('<int:id>', views.book_detail, name='book-detail'),
]
