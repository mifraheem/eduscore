from django.shortcuts import render

def student_dashboard(request):
    return render(request, 'student/dashboard.html')

def classes(request):
    return render(request, 'student/classes.html')

def class_view(request, class_id):
    return render(request, 'student/class_view.html')

def take_quiz(request):
    return render(request, 'student/take_quiz.html')

def quiz_result(request):
    return render(request, 'student/quiz_result.html')

def profile(request):
    return render(request, 'student/profile.html')

def notifications(request):
    return render(request, 'student/notifications.html')

def quizzes(request):
    return render(request, 'student/quizzes.html')