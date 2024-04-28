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

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LevelInline]

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [VideoInline]

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = [QuizInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass  # No need for inlines for Quiz admin

@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    pass  # No need for inlines for Quiz admin