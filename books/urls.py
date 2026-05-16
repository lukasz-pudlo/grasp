from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('<int:pk>', views.book_detail, name='book-detail'),
    path('add', views.book_add, name='book-add'),
    path('add/submit', views.book_add_submit, name='book-add-submit'),
    path('add/cancel', views.book_add_cancel, name='book-add-cancel'),
    path('<int:pk>/edit', views.book_edit, name='book-edit'),
    path('<int:pk>/edit/submit', views.book_edit_submit, name='book-edit-submit'),
    path('fragment/<int:pk>', views.fragment_detail, name="fragment-detail"),
    path('fragment/<int:pk>/sentences',
         views.sentence_list, name='sentence-list'),
    path('sentence/<int:pk>/words', views.word_list, name='word-list'),
    path('words/<int:pk>/learn/<round>', views.learn_words, name="learn-words"),
    path('words/reveal/<int:pk>',
         views.reveal_word, name="reveal-word"),
    path('words/review/<int:pk>',
         views.review_words, name="review-words"),
    path('words/review/<int:pk>/input',
         views.input_review_word, name="input-review-word"),
    # If you want those to appear in address bar, use hx-boost
    path('words/verify/<int:pk>',
         views.verify_word, name="verify-word"),
    path('words/invisible/<int:pk>',
         views.invisible_word, name="invisible-word"),
]
