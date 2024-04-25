from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to="Course_img", blank=True, null=True)
    professor = models.ForeignKey("Users.Professor", on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    members_count = models.IntegerField(default=0)

    def update_members_count(self):
        self.members_count = self.enrolled_users.count()
        self.save()

    def __str__(self):
        return self.title

class Level(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='levels')
    image = models.ImageField(upload_to="levels_images", blank=True, null=True)
    level_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def videos_count(self):
        modules = self.modules.all()
        total_videos = 0
        for module in modules:
            total_videos += module.videos.count()
        return total_videos

    def update_completion_status(self, user):
        user_progress = UserCourseProgress.objects.get(user=user, course=self.course)
        if all(module in user_progress.completed_modules.all() for module in self.modules.all()):
            user_progress.completed_levels.add(self)
            self.course.update_completion_status(user)

class Module(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    module_number = models.IntegerField(blank=True, null=True)
    description = models.TextField()

    def update_completion_status(self, user):
        user_progress = UserCourseProgress.objects.get(user=user, course=self.level.course)
        if all(video in user_progress.completed_videos.all() for video in self.videos.all()):
            user_progress.completed_modules.add(self)
            self.level.update_completion_status(user)

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="coursesVideos", max_length=100, blank=True, null=True)
    summary = models.JSONField(default=dict)
    notes = models.JSONField(default=dict)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.module:
            self.module.update_completion_status()

class Quiz(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='quiz')
    question = models.TextField()
    options = models.JSONField()

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quizzes = models.ManyToManyField(Quiz)

class UserCourseProgress(models.Model):
    user = models.ForeignKey("Users.CustomUser", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_levels = models.ManyToManyField(Level, blank=True, related_name='completed_levels')
    completed_modules = models.ManyToManyField(Module, blank=True, related_name='completed_modules')
    completed_videos = models.ManyToManyField(Video, blank=True, related_name='completed_videos')

    def update_completion_status(self, user):
        user_progress = UserCourseProgress.objects.get(user=user, course=self.course)
        if all(level in user_progress.completed_levels.all() for level in self.course.levels.all()):
            user_progress.completed = True
            user_progress.save()
            
class LevelProgression(models.Model):
    user = models.ForeignKey("Users.CustomUser", on_delete=models.CASCADE, blank=True, related_name='level_progressions')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, related_name='progressions')
    progress = models.IntegerField(default=0, null=True, blank=True)

class CourseProgression(models.Model):
    user = models.ForeignKey("Users.CustomUser", on_delete=models.CASCADE, blank=True, related_name='course_progressions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, related_name='user_progressions')

    def calculate_progression(self):
        course_levels = self.course.levels.all()
        level_progressions = LevelProgression.objects.filter(level__in=course_levels, user=self.user)
        total_progress = level_progressions.aggregate(Sum('progress'))['progress__sum']
        total_progress = total_progress or 0
        print('Total progress', total_progress)
        return total_progress
