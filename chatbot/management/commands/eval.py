import json
import logging
import os
import time
from datetime import datetime

import openai
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from todo.models import Task
from chatbot.utils import take_action_against_task
from chatbot.views import get_all_tasks, get_chat_response, get_task, assign_to_employee
from chatbot.management.commands.agent import assign_category_to_task

load_dotenv()

client = openai.Client()
client.api_key = os.getenv("OPENAI_API_KEY")

questions = [
    ("What types of handyman services do you offer?", 1, 1),
    ("How soon can I schedule an appointment?", 2, 1),
    ("Do you provide free estimates?", 2, 1),
    ("What are your rates? Do you charge by the hour or per job?", 2, 1),
    ("Are your handymen licensed and insured?", 1, 0),
    ("Do you offer emergency or same-day services?", 1, 1),
    ("What areas do you service?", 1, 1),
    ("Can you provide references or customer reviews?", 1, 0),
    ("Do you bring your own tools and materials, or do I need to supply them?", 1, 0),
    ("What forms of payment do you accept?", 2, 1),
    ("Is there a minimum charge for small jobs?", 2, 1),
    ("Do you offer discounts for senior citizens or veterans?", 2, 1),
    ("How do you handle unexpected repairs or additional costs?", 2, 1),
    ("Can I request a specific handyman for my job?", 1, 1),
    ("What’s your cancellation or rescheduling policy?", 1, 0),
    ("Do you offer any guarantees or warranties on your work?", 1, 0),
    ("Can you help with both interior and exterior repairs?", 1, 0),
    ("Do you offer any maintenance plans or regular service contracts?", 1, 1),
    ("What are your business hours?", 1, 1),
    ("How far in advance should I book an appointment?", 1, 0),
]


def chat(text):
    conversation = [
        {"role": "user", "content": text},
    ]
    tasks = get_all_tasks()
    response = get_chat_response(conversation)
    todo_items = get_task(conversation, tasks)
    for item in todo_items:
        assign_to_employee(item)


class Command(BaseCommand):
    help = "Evalulate bot"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting tasks")
        Task.objects.all().delete()

        global questions
        expected_tasks = sum([x[1] for x in questions])
        expected_ai_tasks = sum([x[2] for x in questions])
        questions = [x[0] for x in questions]

        self.stdout.write("Asking questions from the chatbot")
        for question in questions:
            chat(question)

        tasks = Task.objects.filter(completed=False, assigned_to__employee_type="ai")
        task_created = tasks.count()

        for task in tasks:
            category = assign_category_to_task(task)
            take_action_against_task(task, category)

        task_completed = Task.objects.filter(completed=True).count()

        self.stdout.write(f"Questions asked: {len(questions)}")
        self.stdout.write(f"Tasks created: {task_created}")
        self.stdout.write(f"Expected Tasks created: {expected_tasks}")
        self.stdout.write(f"Tasks completed by AI: {task_completed}")
        self.stdout.write(f"Expected Tasks completed by AI: {expected_ai_tasks}")
