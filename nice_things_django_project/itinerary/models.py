import datetime

from django.db import models
from django.utils import timezone

# Classes Question and Choice are just
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now()


datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Business(models.Model):
    """
    """
    business_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()


class Flag(models.Model):
    """

    """
    flag_type = models.CharField(max_length=200)