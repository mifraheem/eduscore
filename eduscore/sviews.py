from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import role
from courses.models import Course, Enrollment, Material
from users.models import User
from quizzes.models import Quiz, QuizAttempt  # uncomment later when quiz model added
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import role
from courses.models import Course, Enrollment, Material
from quizzes.models import Quiz, Question, QuizAttempt
from users.models import User

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
    """Student view for class details, materials, quizzes, performance, classmates."""

    course = get_object_or_404(Course, id=class_id)

    # Ensure student is part of the class
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    # ---------- MATERIALS ----------
    materials = Material.objects.filter(course=course).order_by("-uploaded_at")

    # ---------- CLASSMATES ----------
    classmates = User.objects.filter(
        enrollments__course=course,
        role="student"
    ).exclude(id=request.user.id).distinct()

    # ---------- QUIZZES ----------
    quizzes = Quiz.objects.filter(course=course).order_by("-created_at")

    quiz_rows = []
    for quiz in quizzes:
        attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz).first()

        if attempt:
            status = "Completed"
            score = attempt.score
        else:
            status = "Pending"
            score = None

        quiz_rows.append({
            "id": quiz.id,
            "title": quiz.title,
            "questions": quiz.questions.count(),
            "status": status,
            "score": score,
        })

    # ---------- PERFORMANCE ----------
    attempts = QuizAttempt.objects.filter(student=request.user, quiz__course=course)

    if attempts.exists():
        highest = attempts.order_by("-score").first().score
        lowest = attempts.order_by("score").first().score
        average = round(sum(a.score for a in attempts) / attempts.count(), 2)

        history = [
            {
                "quiz": a.quiz.title,
                "date": a.created_at.strftime("%b %d, %Y"),
                "score": a.score,
                "feedback": a.feedback or "No feedback"
            }
            for a in attempts.order_by("-created_at")
        ]
    else:
        highest = 0
        lowest = 0
        average = 0
        history = []

    performance = {
        "highest": highest,
        "lowest": lowest,
        "average": average,
        "history": history,
    }

    return render(request, "student/class_view.html", {
        "course": course,
        "materials": materials,
        "classmates": classmates,
        "quizzes": quiz_rows,
        "performance": performance,
    })



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
def std_take_quiz(request, quiz_id):
    """Display quiz to student and evaluate answers."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Must be enrolled in this class
    if not Enrollment.objects.filter(course=quiz.course, student=request.user).exists():
        messages.error(request, "You are not enrolled in this class.")
        return redirect("std_classes")

    # Already attempted?
    attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz).first()
    if attempt:
        return redirect("std_quiz_result", attempt_id=attempt.id)

    questions = quiz.questions.all()

    # -------- POST: Submit Quiz -------- #
    if request.method == "POST":
        total_score = 0
        obtained_score = 0

        for q in questions:
            total_score += q.marks
            selected = request.POST.get(f"q{q.id}")

            if selected and selected == q.correct_option:
                obtained_score += q.marks

        # Save attempt
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=obtained_score,
            total_marks=total_score,
            feedback="Auto-evaluated."
        )

        return redirect("std_quiz_result", attempt_id=attempt.id)

    return render(request, "student/take_quiz.html", {
        "quiz": quiz,
        "questions": questions,
    })

@login_required
@role('student')
def std_quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)

    return render(request, "student/quiz_result.html", {
        "attempt": attempt,
        "quiz": attempt.quiz,
        "course": attempt.quiz.course,
    })


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
