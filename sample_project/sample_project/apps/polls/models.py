import datetime
import uuid

from django.db import models
from django.utils import timezone

from ognajd.models import VersioningMeta


class Tags(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid.uuid4,
        editable=True,
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):

    class VersioningMeta(VersioningMeta):
        save_empty_changes = False

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    tags = models.ManyToManyField(
        Tags,
        editable=True,
        blank=True,
    )

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choises')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
