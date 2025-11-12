from django.shortcuts import render

def home(request):
    return render(request, 'teacher/home.html')

def teacher_classes(request):
    return render(request, 'teacher/classes.html')

def class_view(request, class_id):
    return render(request, 'teacher/class_view.html')

def upload_material(request):
    return render(request, 'teacher/upload_material.html')

def generate_quiz(request):
    return render(request, 'teacher/generate_quiz.html')

def quiz_list(request):
    return render(request, 'teacher/quiz_list.html')

def quiz_result(request):
    return render(request, 'teacher/quiz_result.html')

def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')
