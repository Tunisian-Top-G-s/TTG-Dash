# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from asgiref.sync import sync_to_async

from Users.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            customuser_id = text_data_json["customuser_id"]
            print(customuser_id, message, "message hhhhhhhhhhhhhhhhhhhhhhhh")
            # Validate incoming data
            if not message or not customuser_id:
                print("error")
                raise ValueError("Invalid message or customuser_id")

            # Get the CustomUser instance
            customuser = await self.get_user(customuser_id)
            # Save message to database
            await self.save_message(customuser, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message, "username": customuser.first_name}
            )
        except json.JSONDecodeError:
            # Handle JSON decode error
            await self.send_error_message("Invalid JSON format")
        except ValueError as e:
            # Handle value error
            await self.send_error_message(str(e))
        except Exception as e:
            import traceback
            traceback.print_exc()
            await self.send_error_message("An error occurred: " + str(e))

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))

    async def get_user(self, customuser_id):
        try:
            custom_user = await sync_to_async(CustomUser.objects.get)(id=customuser_id)
            return custom_user
        except CustomUser.DoesNotExist:
            print("CustomUser does not exist for the given customuser_id:", customuser_id)
            return None
        except Exception as e:
            print("An error occurred while fetching CustomUser:", str(e))
            return None

    async def save_message(self, customuser, message):
        if customuser:
            await sync_to_async(Message.objects.create)(user=customuser, room_name=self.room_name, content=message)

    async def send_error_message(self, error_message):
        await self.send(text_data=json.dumps({"error": error_message}))