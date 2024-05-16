from django.contrib import admin
from .models import Course, Level, Module, Video, Quiz, UserCourseProgress 

class QuizInline(admin.StackedInline):
    model = Quiz
    

class VideoInline(admin.StackedInline):
    model = Video

class ModuleInline(admin.StackedInline):
    model = Module
    inlines = [VideoInline]
    

class LevelInline(admin.StackedInline):
    model = Level
    inlines = [ModuleInline]
    

class QuizzInline(admin.StackedInline):
    model = Quiz
    

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title','course_image' ,'professor' ,'price' ,'members_count']
    list_per_page = 10
    inlines = [LevelInline, ModuleInline, VideoInline, QuizzInline]

@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    pass  # No need for inlines for Quiz admin
