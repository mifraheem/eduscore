from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import role
from courses.models import Course, Enrollment, Material
from users.models import User
# from quizzes.models import Quiz, QuizAttempt  # uncomment later when quiz model added


@login_required
@role('student')
def student_dashboard(request):
    return render(request, 'student/dashboard.html')


@login_required
@role('student')
def std_classes(request):
    """List all classes joined by the student and handle joining via class code."""
    enrolled_classes = Course.objects.filter(enrollments__student=request.user).distinct()

    # Handle joining new class
    if request.method == 'POST':
        class_code = request.POST.get('class_code', '').strip().upper()

        if not class_code:
            messages.warning(request, "Please enter a valid class code.")
            return redirect('std_classes')

        course = Course.objects.filter(code=class_code).first()
        if not course:
            messages.error(request, f"No class found with code '{class_code}'.")
            return redirect('std_classes')

        # Check if already joined
        if Enrollment.objects.filter(course=course, student=request.user).exists():
            messages.info(request, f"You are already enrolled in {course.title}.")
            return redirect('std_classes')

        Enrollment.objects.create(course=course, student=request.user)
        messages.success(request, f"You have successfully joined '{course.title}'.")
        return redirect('std_classes')

    context = {'enrolled_classes': enrolled_classes}
    return render(request, 'student/classes.html', context)


@login_required
@role('student')
def class_view(request, class_id):
    """Detailed class page for student: materials, classmates, and performance."""
    course = get_object_or_404(Course, id=class_id)
    enrollment = get_object_or_404(Enrollment, course=course, student=request.user)

    # All materials for this course
    materials = Material.objects.filter(course=course).order_by('-uploaded_at')

    # Classmates (exclude current student)
    classmates = User.objects.filter(
        enrollments__course=course, role='student'
    ).exclude(id=request.user.id).distinct()

    # Mock quizzes (to be replaced with real model later)
    quizzes = [
        {"title": "Algebra Basics", "questions": 10, "status": "Completed", "score": 88},
        {"title": "Linear Equations", "questions": 8, "status": "Pending", "score": None},
        {"title": "Geometry Fundamentals", "questions": 7, "status": "Completed", "score": 92},
    ]

    performance = {
        "highest": 95,
        "lowest": 63,
        "average": 81,
        "history": [
            {"quiz": "Algebra Basics", "date": "Oct 5, 2025", "score": 88, "feedback": "Good understanding, minor algebraic errors."},
            {"quiz": "Geometry Fundamentals", "date": "Oct 8, 2025", "score": 92, "feedback": "Excellent grasp of geometry basics."},
            {"quiz": "Trigonometry Practice", "date": "Oct 11, 2025", "score": 75, "feedback": "Needs more work on sine and cosine rules."},
        ]
    }

    context = {
        'course': course,
        'materials': materials,
        'classmates': classmates,
        'quizzes': quizzes,
        'performance': performance,
    }
    return render(request, 'student/class_view.html', context)



@login_required
@role('student')
def leave_class(request, class_id):
    """Allow student to leave a joined class."""
    course = get_object_or_404(Course, id=class_id)
    enrollment = Enrollment.objects.filter(course=course, student=request.user).first()

    if not enrollment:
        messages.error(request, "You are not enrolled in this class.")
        return redirect('std_classes')

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, f"You have left the class '{course.title}'.")
        return redirect('std_classes')

    return redirect('class_view', class_id=course.id)


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
