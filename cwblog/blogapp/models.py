from django.db import models


class Story(models.Model):
    title = models.TextField()
    body = models.TextField()
    date = models.DateTimeField()


class Submission(models.Model):
    story = models.ForeignKey(Story)
    text = models.CharField(max_length=140)
    votes = models.IntegerField(default=0)
    date = models.DateTimeField()


