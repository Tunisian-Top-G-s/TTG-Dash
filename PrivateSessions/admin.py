from django.contrib import admin
from .models import PrivateSession, PrivateSessionRequest
# Register your models here.
admin.site.register(PrivateSession)
admin.site.register(PrivateSessionRequest)