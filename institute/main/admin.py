from django.contrib import admin
from .models import Course, Student

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "fees")
    search_fields = ("title",)
    list_filter = ("fees",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "course", "contact")
    search_fields = ("name", "email")
    list_filter = ("course",)
