from django.urls import path
from .views import (
    quiz_list, create_quiz, add_questions,
    quiz_ai_generate, quiz_ai_preview, quiz_ai_save
)

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('create/', create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add-questions/', add_questions, name='add_questions'),

    # FIXED: changed id → class_id
    path("generate/<int:class_id>/", quiz_ai_generate, name="quiz_ai_generate"),

    path("ai/preview/", quiz_ai_preview, name="quiz_ai_preview"),
    path("ai/save/", quiz_ai_save, name="quiz_ai_save"),
]