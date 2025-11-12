from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from users.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from users.decorators import role
from courses.models import Course, Enrollment, Material
from quizzes.models import Quiz, QuizAttempt


@login_required
@role('teacher')
def teacher_dashboard(request):
    teacher = request.user

    # All courses taught by teacher
    courses = Course.objects.filter(teacher=teacher)

    # Stats
    total_classes = courses.count()
    total_students = Enrollment.objects.filter(course__teacher=teacher).count()
    total_quizzes = Quiz.objects.filter(created_by=teacher).count()
    total_materials = Material.objects.filter(course__teacher=teacher).count()

    # Average score (from quiz attempts)
    attempts = QuizAttempt.objects.filter(
        quiz__created_by=teacher, is_submitted=True)
    if attempts:
        avg_score = round(sum(a.score for a in attempts) / attempts.count(), 1)
    else:
        avg_score = 0

    # Recent classes (limit 4)
    recent_classes = courses.order_by('-created_at')[:4]

    # Recent quizzes (limit 5)
    recent_quizzes = Quiz.objects.filter(
        created_by=teacher).order_by('-created_at')[:5]

    # Student activity (limit 5)
    recent_activity = QuizAttempt.objects.filter(
        quiz__created_by=teacher,
        is_submitted=True
    ).select_related('quiz', 'student').order_by('-submitted_at')[:5]

    context = {
        "total_classes": total_classes,
        "total_students": total_students,
        "total_quizzes": total_quizzes,
        "total_materials": total_materials,
        "avg_score": avg_score,
        "recent_classes": recent_classes,
        "recent_quizzes": recent_quizzes,
        "recent_activity": recent_activity,
    }
    return render(request, "teacher/dashboard.html", context)


@login_required
@role('teacher')
def teacher_classes(request):
    """Create and list teacher's courses."""
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        section = request.POST.get('section')
        description = request.POST.get('description')

        if not title:
            messages.warning(request, "Class name is required.")
            return redirect('classes')

        code = f"{subject[:3].upper()}{get_random_string(3).upper()}"
        Course.objects.create(
            teacher=request.user,
            title=title,
            code=code,
            description=f"{subject} – Section {section}. {description or ''}"
        )
        messages.success(request, f"Class '{title}' created successfully!")
        return redirect('classes')

    classes = Course.objects.filter(
        teacher=request.user).order_by('-created_at')
    return render(request, 'teacher/classes.html', {'classes': classes})


@login_required
@role('teacher')
def teacher_class_view(request, class_id):
    """Detailed class view with add-student functionality."""
    course = get_object_or_404(Course, id=class_id, teacher=request.user)
    students = Enrollment.objects.filter(
        course=course).select_related('student')
    materials = Material.objects.filter(course=course).order_by('-uploaded_at')

    # Add students by email (comma-separated)
    if request.method == 'POST':
        emails_raw = request.POST.get('emails')
        if emails_raw:
            emails = [e.strip().lower()
                      for e in emails_raw.split(',') if e.strip()]
            added, skipped = [], []

            for email in emails:
                student = User.objects.filter(
                    email=email, role='student').first()
                if not student:
                    skipped.append(email)
                    continue
                if Enrollment.objects.filter(student=student, course=course).exists():
                    skipped.append(email)
                    continue
                Enrollment.objects.create(student=student, course=course)
                added.append(email)

            if added:
                messages.success(request, f"Enrolled: {', '.join(added)}")
            if skipped:
                messages.warning(
                    request, f"Skipped (not found or already added): {', '.join(skipped)}")
            return redirect('class_view', class_id=course.id)

    context = {
        'course': course,
        'students': students,
        'materials': materials,
        'total_students': students.count(),
        'total_materials': materials.count(),
        'pending_quizzes': 0,  # placeholder for quiz integration
    }
    return render(request, 'teacher/class_view.html', context)


@login_required
@role('teacher')
def upload_material(request):
    """Upload study materials for a course."""
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if not (course_id and title and file):
            messages.error(request, "All fields are required.")
            return redirect('upload_material')

        course = get_object_or_404(Course, id=course_id, teacher=request.user)
        Material.objects.create(course=course, title=title, file=file)
        messages.success(request, f"Material '{title}' uploaded successfully!")
        return redirect('upload_material')

    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'teacher/upload_material.html', {'courses': courses})


@login_required
@role('teacher')
def generate_quiz(request):
    """Future integration: quiz generation via n8n."""
    messages.info(request, "Quiz generation via n8n integration coming soon.")
    return render(request, 'teacher/generate_quiz.html')


@login_required
@role('teacher')
def quiz_list(request):
    """Placeholder for teacher's quizzes."""
    return render(request, 'teacher/quiz_list.html')


@login_required
@role('teacher')
def quiz_result(request):
    """Placeholder for quiz results."""
    return render(request, 'teacher/quiz_result.html')


@login_required
@role('teacher')
def home(request):
    """Redirect teacher home to dashboard."""
    return redirect('teacher_dashboard')
