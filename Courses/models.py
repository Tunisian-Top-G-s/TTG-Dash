from django.db import models
from django.db.models import Sum

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to="Course_img", blank=True, null=True)
    professor = models.ForeignKey("Users.Professor", on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    members_count = models.IntegerField(default=0)

    def course_progression(self, user):
        try:
            progression = CourseProgression.objects.get(course=self, user=user)
            return progression
        except CourseProgression.DoesNotExist:
            return None

    def update_members_count(self):
        self.members_count = self.enrolled_users.count()
        self.save()

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

class Module(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    module_number = models.IntegerField(blank=True, null=True)
    description = models.TextField()

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="coursesVideos", max_length=100, blank=True, null=True)
    summary = models.JSONField(default=dict)
    notes = models.JSONField(default=dict)
    finished = models.BooleanField(default=False)

class Quiz(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='quiz')
    question = models.TextField()
    options = models.JSONField()
    answer = models.IntegerField(blank=True, null=True)

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quizzes = models.ManyToManyField(Quiz)

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
