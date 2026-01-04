from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    gender_choices = (
        ('m', 'male'),
        ('f', 'female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=gender_choices, null=True, blank=True)


class Relations(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'
