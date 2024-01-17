from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    prompt = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
