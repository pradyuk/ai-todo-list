from django.db import models


class Employee(models.Model):
    EMPLOYEE_TYPE_CHOICES = [
        ("human", "Human Employee"),
        ("ai", "AI Employee"),
    ]

    name = models.CharField(max_length=255)
    employee_type = models.CharField(max_length=10, choices=EMPLOYEE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_employee_type_display()})"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.employee.name} on {self.task.title}"
