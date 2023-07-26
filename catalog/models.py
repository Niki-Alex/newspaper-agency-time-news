from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0, message="Years of experience cannot be negative!")]
    )

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    # def get_absolute_url(self):
    #     return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="newspapers")
    publishers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="newspapers")

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"Topic {self.topic}\n"
            f"Published date: {self.published_date}\n"
            f"Publishers: {self.publishers}"
        )
