from django.db import models
from django.contrib.auth.models import User


class Story(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()
    date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    story = models.ForeignKey(Story)
    text = models.CharField(max_length=140)
    votes = models.IntegerField(default=0)
    date = models.DateTimeField()
    author = models.ForeignKey(User, related_name='author')
    voted_on = models.ManyToManyField(User, related_name='voter')

    def __str__(self):
        return self.text


