from django.contrib import admin
from .models import Course, Enrollment, Material


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'teacher', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'code', 'teacher__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Course Info', {
            'fields': ('title', 'code', 'description')
        }),
        ('Teacher & Meta', {
            'fields': ('teacher', 'created_at')
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'joined_on')
    list_filter = ('joined_on', 'course')
    search_fields = ('student__email', 'course__title')
    ordering = ('-joined_on',)
    readonly_fields = ('joined_on',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_at')
    list_filter = ('uploaded_at', 'course')
    search_fields = ('title', 'course__title')
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at',)
