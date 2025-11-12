from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from .tviews import *
from .sviews import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home, name='home'),
    path('auth/', include('users.urls')),
    path('classes/', teacher_classes, name='classes'),
    path('classes/<int:class_id>/', teacher_class_view, name='class_view'),
    path('upload-material/', upload_material, name='upload_material'),
    path('generate-quiz/', generate_quiz, name='generate_quiz'),
    path('quiz-list/', quiz_list, name='quiz_list'),
    path('quiz-result/', quiz_result, name='quiz_result'),
    path('dashboard/', teacher_dashboard, name='teacher_dashboard'),

    path('', student_dashboard, name='student_dashboard'),
    path('student/classes/', classes, name='std_classes'),
    path('student/classes/<int:class_id>/', class_view, name='std_class_view'),
    path('student/take-quiz/', take_quiz, name='std_take_quiz'),
    path('student/quiz-result/', quiz_result, name='std_quiz_result'),
    path('student/profile/', profile, name='student_profile'),
    path('student/notifications/', notifications, name='std_notifications'),
    path('student/quizzes/', quizzes, name='std_quizzes'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)