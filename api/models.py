from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db import models
from django.contrib.auth.models import AbstractUser


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Custom fields and methods

    # Set unique related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')



class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user.username} for exercise {self.exercise.name}"
