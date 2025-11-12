from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import role
from courses.models import Course
from .models import Quiz, Question


@login_required
@role('teacher')
def quiz_list(request):
    """List all quizzes created by the logged-in teacher."""
    quizzes = Quiz.objects.filter(created_by=request.user).select_related('course').order_by('-created_at')
    return render(request, 'teacher/quiz_list.html', {'quizzes': quizzes})


@login_required
@role('teacher')
def create_quiz(request):
    """Manual quiz creation (without Django forms)."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        time_limit = request.POST.get('time_limit')
        course_id = request.POST.get('course')

        if not title or not course_id:
            messages.warning(request, "Title and course are required.")
            return redirect('create_quiz')

        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        quiz = Quiz.objects.create(
            course=course,
            title=title,
            description=description or '',
            time_limit=time_limit or 10,
            created_by=request.user
        )

        messages.success(request, f"Quiz '{quiz.title}' created successfully!")
        return redirect('add_questions', quiz_id=quiz.id)

    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'teacher/create_quiz.html', {'courses': courses})


@login_required
@role('teacher')
def add_questions(request, quiz_id):
    """Add multiple questions manually to an existing quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)

    if request.method == 'POST':
        text = request.POST.get('text')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        correct_option = request.POST.get('correct_option')
        marks = request.POST.get('marks', 1)

        if not text or not correct_option:
            messages.warning(request, "Please fill in all required fields.")
            return redirect('add_questions', quiz_id=quiz.id)

        Question.objects.create(
            quiz=quiz,
            text=text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
            marks=marks
        )
        messages.success(request, "Question added successfully!")
        return redirect('add_questions', quiz_id=quiz.id)

    questions = quiz.questions.all()
    return render(request, 'teacher/add_questions.html', {'quiz': quiz, 'questions': questions})
