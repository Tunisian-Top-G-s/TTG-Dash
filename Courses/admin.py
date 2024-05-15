from django.contrib import admin
from .models import Course, Level, Module, Video, Quiz, UserCourseProgress 

class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 1

class VideoInline(admin.StackedInline):
    model = Video
    extra = 1

class ModuleInline(admin.StackedInline):
    model = Module
    inlines = [VideoInline]
    extra = 1

class LevelInline(admin.StackedInline):
    model = Level
    inlines = [ModuleInline]
    extra = 1

class QuizzInline(admin.StackedInline):
    model = Quiz
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title','course_image' ,'professor' ,'price' ,'members_count']
    list_per_page = 10
    inlines = [LevelInline, ModuleInline, VideoInline, QuizzInline]

@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    pass  # No need for inlines for Quiz admin
