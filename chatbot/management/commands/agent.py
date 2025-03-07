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

load_dotenv()

client = openai.Client()
client.api_key = os.getenv("OPENAI_API_KEY")
print("key",client.api_key)


def assign_category_to_task(task):
    prompt = """
    Your task is to assign a category to a task. Here are the categories:
    - Services
    - Pricing
    - Schedule Visit
    - Visit
    - Schedule Meeting
    - Talk
    """
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": task.title,
        },
    ]

    completion = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return completion.choices[0].message.content


class Command(BaseCommand):
    help = "Accomplish tasks"

    def handle(self, *args, **kwargs):

        while True:
            tasks = Task.objects.filter(
                completed=False, assigned_to__employee_type="ai"
            )

            if not tasks.exists():
                self.stdout.write(
                    self.style.WARNING("No tasks to complete. Sleeping for 1 second...")
                )
                time.sleep(1)
                continue

            for task in tasks:
                category = assign_category_to_task(task)
                print(f"{task.title} - {category}")
                take_action_against_task(task, category)

            time.sleep(1)
