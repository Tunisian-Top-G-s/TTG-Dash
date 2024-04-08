# Chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message, Room
from django.core.serializers import serialize  # Import Django's default serializer
from django.core.cache import cache  # Import Django's cache module

from asgiref.sync import sync_to_async

from Users.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.customuser_id = self.scope['user'].id  # Assuming you have authenticated users

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Set user as online
        await self.set_user_online()

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Set user as offline
        await self.set_user_offline()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            # Validate incoming data
            if not message:
                raise ValueError("Invalid message")

            # Save message to database
            message_instance = await self.save_message(message)
            serialized_message = serialize('json', [message_instance])  # Serialize the message instance

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message, "username": self.scope['user'].username, "instance": serialized_message}
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
        serialized_message = event["instance"]  # Get the serialized message
        username = event["username"]  # Get the username
    
        try:
            # Fetch user profile picture (pfp)
            user_id = json.loads(event["instance"])[0]["fields"]["user"]
            print(user_id)
            pfp_url = await self.get_user_pfp(user_id)
    
            # Send message, username, profile picture, and serialized message to WebSocket
            await self.send(text_data=json.dumps({
                "message": message,
                "username": username,
                "pfp": pfp_url,
                "instance": serialized_message
            }))
        except Exception as e:
            # Handle any errors
            print("An error occurred:", str(e))
    
    async def get_user_pfp(self, user_id):
        try:
            custom_user = await sync_to_async(CustomUser.objects.get)(id=user_id)
            return custom_user.pfp.url if custom_user.pfp else None
        except CustomUser.DoesNotExist:
            print("CustomUser does not exist for the given user_id:", user_id)
            return None
        except Exception as e:
            print("An error occurred while fetching profile picture:", str(e))
            return None

    async def save_message(self, message):
        customuser = await self.get_user()
        if customuser:
            room = await self.get_room(self.room_name)
            saved_message = await sync_to_async(Message.objects.create)(user=customuser, room=room, content=message)
            return saved_message

    async def get_user(self):
        try:
            custom_user = await sync_to_async(CustomUser.objects.get)(id=self.customuser_id)
            return custom_user
        except CustomUser.DoesNotExist:
            print("CustomUser does not exist for the given customuser_id:", self.customuser_id)
            return None
        except Exception as e:
            print("An error occurred while fetching CustomUser:", str(e))
            return None

    async def get_room(self, room_name):
        try:
            room = await sync_to_async(Room.objects.get)(name=room_name)
            return room
        except Room.DoesNotExist:
            print("Room does not exist for the given room_name:", room_name)
            return None
        except Exception as e:
            print("An error occurred while fetching Room:", str(e))
            return None

    async def send_error_message(self, error_message):
        await self.send(text_data=json.dumps({"error": error_message}))

    async def set_user_online(self):
        # Set user as online for 30 seconds in cache
        cache.set(f'user_{self.customuser_id}_online', True, timeout=30)

    async def set_user_offline(self):
        # Set user as offline
        cache.delete(f'user_{self.customuser_id}_online')