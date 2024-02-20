from django.contrib import admin
from .models import Course, Level, Video, Quiz, Exam, LevelProgression, CourseProgression, Module
# Register your models here.
admin.site.register([Course, Level, Video, Quiz, Exam, LevelProgression, CourseProgression, Module])

