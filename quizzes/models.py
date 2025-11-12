from django.db import models
from django.utils import timezone
from users.models import User
from courses.models import Course


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_marks = models.PositiveIntegerField(default=0)
    time_limit = models.PositiveIntegerField(default=10)  # minutes
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    class Meta:
        ordering = ['-created_at']


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_option = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        ]
    )

    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Q{self.id}: {self.text[:40]}..."


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')

    started_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)

    score = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)        # ✅ added
    feedback = models.TextField(blank=True, null=True) # ✅ added

    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('quiz', 'student')
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student.email} → {self.quiz.title}"


class StudentAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        null=True,
        blank=True
    )

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attempt.student.email} - {self.question.text[:30]}"

    class Meta:
        ordering = ['question__id']
