from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

EMAIL_MAX_LENGTH = 256


class Ticket(models.Model):
    class Status(models.TextChoices):
        NEW = "new"
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        DONE = "done"

    email = models.EmailField(max_length=EMAIL_MAX_LENGTH)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=8, choices=Status.choices, default=Status.NEW
    )

    def __str__(self):
        return "{}, {}, {}".format(self.email, self.date, self.description)
