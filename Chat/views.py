# chat/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Message
from Users.models import CustomUser
from django.core.serializers.json import DjangoJSONEncoder
import json

def send_message(request):
    if request.method == "POST":
        customuser_id = request.POST.get("customuser_id")
        room_name = request.POST.get("room_name")
        content = request.POST.get("content")

        user = get_object_or_404(CustomUser, id=customuser_id)
        
        if user and room_name and content:
            # Create and save the message
            message = Message(user=user, room_name=room_name, content=content)
            message.save()
            return HttpResponse("Message sent successfully!")
        else:
            return HttpResponseBadRequest("Invalid data provided.")
    else:
        return HttpResponseBadRequest("Invalid request method.")


def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    customuser_id = request.user.customuser.id
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp').values('user__first_name', 'content')
    messages_list = list(messages)
    
    # Convert QuerySet to list of dictionaries
    messages_list = [dict(message) for message in messages_list]

    # Serialize the messages list to JSON
    messages_json = json.dumps(messages_list, cls=DjangoJSONEncoder)

    print(messages_json)  # Add this line for debugging
    return render(request, "chat/room.html", {"room_name": room_name, "customuser_id": customuser_id, "messages_json": messages_json})