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


def assign_category_to_task(task):
    prompt = """
    You are a helpful AI chatbot posing as a handyman's receptionist.
    Your job is to assign category to a task. Here are the rules:

    - if the task is about sending email with services information, assign Service Email
    - if the task can be completed by sending services information, assign Service Email
    - if the task is about sending email with pricing information, assign Pricing Email
    - if the task can be completed by sending pricing information, assign Pricing Email
    - if the task is about scheduling visit, assign Schedule Visit
    - if the task can be completed by scheduling a visit, assign Schedule Visit
    - if the task is about visiting customer, assign Visit
    - if the task can be completed by visiting a customer, assign Visit
    - if the task is about scheduling meeting, assign Schedule Meeting
    - if the task can be completed by scheduling a meeting, assign Schedule Meeting
    - if the task is about talking to customer, assign Talk
    - if the task can be completed by talking to a customer, assign Talk

    Do not explain yourself. Your answer should only be from the following list:
    - Service Email
    - Pricing Email
    - Schedule Visit
    - Visit
    - Schedule Meeting
    - Talk
    - Uncategorized
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
