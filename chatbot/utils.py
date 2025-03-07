from todo.models import Employee, Task, Comment


def assign_to_employee(task):
    employee = Employee.objects.filter(
        employee_type="ai",
    ).get()

    Task.objects.create(
        title=task,
        assigned_to=employee,
    )


def get_all_tasks():
    return [x.title for x in Task.objects.all()]


def take_action_against_task(task, category):
    human = Employee.objects.filter(employee_type="human").first()

    if category == "Services":
        task.comments.create(
            employee=task.assigned_to,
            content="Email sent with services information",
        )
        task.completed = True
        task.save()

    elif category == "Pricing":
        task.comments.create(
            employee=task.assigned_to,
            content="Email sent with pricing information",
        )
        task.completed = True
        task.save()
    elif category == "Schedule Visit":
        task.comments.create(employee=task.assigned_to, content="Visit scheduled")
        task.completed = True
        task.save()
    elif category == "Visit":
        task.comments.create(
            employee=task.assigned_to,
            content="Assigning this task to human because I cannot visit.",
        )
        task.assigned_to = human
        task.save()
    elif category == "Schedule Meeting":
        task.comments.create(employee=task.assigned_to, content="Meeting scheduled")
        task.completed = True
        task.save()
    elif category == "Talk":
        task.comments.create(
            employee=task.assigned_to,
            content="Assigning this task to human because I cannot talk.",
        )
        task.assigned_to = human
        task.save()
    else:
        task.comments.create(
            employee=task.assigned_to,
            content=f"Assigning it to {human.name} because I cannot understand this task.",
        )
        task.assigned_to = human
        task.save()
