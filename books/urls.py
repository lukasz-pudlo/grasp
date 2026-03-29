from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('<int:pk>', views.book_detail, name='book-detail'),
    path('<int:pk>/edit', views.book_edit, name='book-edit'),
    path('<int:pk>/edit/submit', views.book_edit_submit, name='book-edit-submit'),
]
