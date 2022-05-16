import uuid

from django.contrib.auth.models import User
from django.db import models
from martor.models import MartorField
from smart_selects.db_fields import ChainedForeignKey

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    objective = MartorField(blank=True, null=True)
    project_information = MartorField(blank=True, null=True)
    def __str__(self):
        return self.name


class Report(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    short_description = models.TextField(blank=True, null=True)
    description = MartorField(null=True, blank=True)

    def __str__(self):
        return self.name

class Target(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.name





class Entry(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    target = ChainedForeignKey(
        Target,
        chained_field="project",
        chained_model_field="project",
        show_all=False,
        auto_choose=True,
        sort=True
    )

    risk_score = models.IntegerField(default=5)
    description = MartorField()
    solution = MartorField()
    more_info = ChainedForeignKey(
        Report,
        chained_field="project",
        chained_model_field="project",
        show_all=False,
        auto_choose=True,
        sort=True,
        default=None,
        blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name





class DomainCredentials(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    domain =  models.URLField()
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.domain

    # def get_len_credentials(self):
    #     return len(self.data) if self.data else 0


