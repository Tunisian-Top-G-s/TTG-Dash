from django.db import models
from django.db.models import Sum

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to="Course_img", blank=True, null=True)
    professor = models.ForeignKey("Users.CustomUser", on_delete=models.CASCADE, related_name='professor_course', null=True, blank=True)
    members_count = models.IntegerField(default=0)  # New field to track members count

    def course_progression(self, user):
        """
        Retrieve CourseProgression for a given user and course.
        """
        try:
            # Attempt to retrieve the CourseProgression instance for the user and current course
            progression = CourseProgression.objects.get(course=self, user=user)
            return progression
        except CourseProgression.DoesNotExist:
            return None

    def update_members_count(self):
        self.members_count = self.enrolled_users.count()
        self.save()

class Level(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="levels_images", blank=True, null=True)
    level_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()

class Module(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    module_number = models.IntegerField(blank=True, null=True)
    description = models.TextField()

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    notes = models.JSONField(default=dict)

class Quiz(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    question = models.TextField()
    options = models.JSONField()
    correct_option = models.JSONField()

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quizzes = models.ManyToManyField(Quiz)


class LevelProgression(models.Model):
    user = models.ForeignKey("Users.CustomUser", on_delete=models.CASCADE, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True)
    progress = models.IntegerField(default=0, null=True, blank=True)

class CourseProgression(models.Model):
    user = models.ForeignKey("Users.CustomUser", on_delete=models.CASCADE, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True)

    def calculate_progression(self):
        # Get all levels associated with the course
        course_levels = self.course.level_set.all()

        # Get LevelProgression instances where the level is in course_levels
        level_progressions = LevelProgression.objects.filter(level__in=course_levels, user=self.user)

        # Calculate the total progress by summing the progress of all related level_progressions
        total_progress = level_progressions.aggregate(Sum('progress'))['progress__sum']

        # Ensure that total_progress is not None, set it to 0 if it is None
        total_progress = total_progress or 0
        print('Total progress', total_progress)
        return total_progress