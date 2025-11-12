from django.db import models
from django.conf import settings
from django.utils import timezone


class Course(models.Model):
    """A course created and managed by a teacher."""
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='courses'
    )
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.code})"


class Enrollment(models.Model):
    """Links students to the courses they join."""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    joined_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.email} → {self.course.title}"


class Material(models.Model):
    """Learning materials uploaded by teachers."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to='materials/')
    summary = models.TextField(blank=True, null=True)  # returned from n8n AI
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.course.title}"
