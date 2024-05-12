from django.contrib import admin
from .models import Dashboard, Home, Feedback, Podcast, Quest, Step, UserQuestProgress, featuredYoutubeVideo
# Register your models here.
admin.site.register(Dashboard)
admin.site.register(Home)
admin.site.register(Podcast)
admin.site.register(Feedback)
admin.site.register(featuredYoutubeVideo)
admin.site.register(Quest)
admin.site.register(Step)
admin.site.register(UserQuestProgress)