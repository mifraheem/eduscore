from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import role


@login_required
@role('student')
def student_dashboard(request):
    return render(request, 'student/dashboard.html')


@login_required
@role('student')
def classes(request):
    return render(request, 'student/classes.html')


@login_required
@role('student')
def class_view(request, class_id):
    return render(request, 'student/class_view.html')


@login_required
@role('student')
def take_quiz(request):
    return render(request, 'student/take_quiz.html')


@login_required
@role('student')
def quiz_result(request):
    return render(request, 'student/quiz_result.html')


@login_required
@role('student')
def profile(request):
    return render(request, 'student/profile.html')


@login_required
@role('student')
def notifications(request):
    return render(request, 'student/notifications.html')


@login_required
@role('student')
def quizzes(request):
    return render(request, 'student/quizzes.html')
