from django.urls import path
from .views import quiz_list, create_quiz, add_questions

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('create/', create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-questions/', add_questions, name='add_questions'),
]