from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contest(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Submission(models.Model):
    image_url = models.URLField(blank=False, null=False)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    score = models.SmallIntegerField()

    def __str__(self):
        return "%s: %s" % (self.user, self.submission)


