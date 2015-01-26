from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title


class Submission(models.Model):
    story = models.ForeignKey(Story)
    text = models.CharField(max_length=140)
    votes = models.IntegerField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return self.text


