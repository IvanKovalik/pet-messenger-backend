from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User

from uuid import uuid4

# Create your models here.
class Profile(models.Model):
    uid = models.UUIDField(
        _("This is uuid of profile"),
        default=uuid4,
        unique=True,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        models.CASCADE,
        help_text='This is User account realated to Profile'
    )
    avatar = models.ImageField(
        default='media/default.jpg',
        upload_to='profile_images',
        help_text='This is avatar to this user profile'    
    )
    date_created = models.DateTimeField(
        _("This is datetime when was created"),
        auto_now_add=True,
    )
    date_changed = models.DateTimeField(
        _("This is when profile was last changed"),
        auto_now=True,
    )

    bio = models.TextField(
        _("This is users's bio"),
        max_length=2000,   
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        ordering = ['uid']
    
    def __str__(self):
        return self.uid
    