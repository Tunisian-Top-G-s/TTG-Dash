from django.contrib import admin
from .models import Dashboard, Home, Feedback, Podcast
# Register your models here.
admin.site.register(Dashboard)
admin.site.register(Home)
admin.site.register(Podcast)
admin.site.register(Feedback)