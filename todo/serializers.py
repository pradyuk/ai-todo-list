from rest_framework import serializers
from .models import Employee, Task, Comment


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="employee", write_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "task", "employee", "employee_id", "content", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = EmployeeSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "assigned_to_id",
            "completed",
            "created_at",
            "comments",
        ]

    def create(self, validated_data):
        """
        Assign new tasks to an AI employee by default.
        """
        ai_employee = Employee.objects.filter(employee_type="ai").first()

        if not ai_employee:
            raise serializers.ValidationError({"assigned_to": "No AI employee found"})

        validated_data["assigned_to"] = ai_employee
        return super().create(validated_data)
