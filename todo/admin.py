from django.contrib import admin
from .models import Employee, Task, Comment


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "employee_type")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "completed", "created_at")
    list_filter = ("completed",)
    search_fields = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "employee", "created_at")
    search_fields = ("content",)
