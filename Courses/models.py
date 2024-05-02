from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.html import mark_safe


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to="Course_img", blank=True, null=True)
    professor = models.ForeignKey("Users.Professor", on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    members_count = models.IntegerField(default=0)

    def course_image(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.img.url))

    def update_members_count(self):
        self.members_count = self.enrolled_users.count()
        self.save()

    def calculate_progress_percentage(self, user):
        total_levels = self.admin_levels.count()
        if total_levels == 0:
            return 0

        user_progress = UserCourseProgress.objects.get(user=user, course=self)
        completed_levels = user_progress.completed_levels.count()
        return (completed_levels / total_levels) * 100

    def __str__(self):
        return self.title

class Level(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_levels', blank=True, null=True)
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

    def calculate_progress_percentage(self, user):
        total_modules = self.modules.count()
        if total_modules == 0:
            return 0

        user_progress = UserCourseProgress.objects.get(user=user, course=self.course)
        completed_modules = user_progress.completed_modules.filter(level=self).count()
        return (completed_modules / total_modules) * 100

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_modules', blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    module_number = models.IntegerField(blank=True, null=True)
    description = models.TextField()

    def update_completion_status(self, user):
        user_progress = UserCourseProgress.objects.get(user=user, course=self.level.course)
        if all(video in user_progress.completed_videos.all() for video in self.videos.all()):
            user_progress.completed_modules.add(self)
            self.level.update_completion_status(user)

    def calculate_progress_percentage(self, user):
        total_videos = self.videos.count()
        if total_videos == 0:
            return 0

        user_progress = UserCourseProgress.objects.get(user=user, course=self.level.course)
        completed_videos = user_progress.completed_videos.filter(module=self).count()
        return (completed_videos / total_videos) * 100

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_videos', blank=True, null=True)
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admin_quiz', blank=True, null=True)
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='quiz')
    question = models.TextField()
    options = models.JSONField()
    answer = models.IntegerField(blank=True, null=True)

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='exams', blank=True, null=True)
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