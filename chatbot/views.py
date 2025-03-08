import os

import openai
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from chatbot.utils import get_all_tasks, assign_to_employee


load_dotenv()

client = openai.Client()
client.api_key = os.getenv("OPENAI_API_KEY")


def get_chat_response(conversation):
    content = (
        "You are a helpful AI chatbot posing as a handyman's receptionist. "
        "If the customer enquires about services, tell the customer that someone will reach out. "
        "If the customer enquires about prices, tell the customer that someone will reach out. "
        "If the customer wants to schedule a visit, tell the customer that someone will reach out. "
        "If the customer wants to talk, tell the customer that someone will reach out. "
    )
    messages = [
        {
            "role": "system",
            "content": content,
        },
    ] + conversation

    completion = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return completion.choices[0].message.content


def get_task(conversation, tasks):
    task_list = "\n".join(tasks)
    prompt = f"""
    You are a helpful AI chatbot posing as a handyman's receptionist.
    Your job is to categorize the message of the customer. Here are the
    categories:
    - Services
    - Pricing
    - Scheduling
    - Talk
    - Unassigned
    """
    content = conversation[-1]["content"]
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": content,
        },
    ]

    completion = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    response = completion.choices[0].message.content
    if response == "Services":
        return ["Send email with services information"]
    elif response == "Pricing":
        return ["Send email pricing information"]
    elif response == "Scheduling":
        return ["Schedule visit", "Visit the customer"]
    elif response == "Talk":
        return ["Schedule meeting", "Talk to customer"]
    else:
        return []


@csrf_exempt
@api_view(["POST"])
def chat_endpoint(request):
    conversation = request.data.get("history")

    if not conversation:
        return Response({"error": "Conversation text is required"}, status=400)

    tasks = get_all_tasks()
    response = get_chat_response(conversation)
    todo_items = get_task(conversation, tasks)
    for item in todo_items:
        assign_to_employee(item)

    return Response({"content": response, "role": "system"})
