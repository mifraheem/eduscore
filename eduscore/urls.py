"""
URL configuration for eduscore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('classes/', teacher_classes, name='classes'),
    path('classes/<int:class_id>/', class_view, name='class_view'),
    path('upload-material/', upload_material, name='upload_material'),
    path('generate-quiz/', generate_quiz, name='generate_quiz'),
    path('quiz-list/', quiz_list, name='quiz_list'),
    path('quiz-result/', quiz_result, name='quiz_result'),
    path('dashboard/', dashboard, name='dashboard'),
]
