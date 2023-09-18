from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4

from ivangram.settings import AUTH_USER_MODEL

# Create your models here.
class Message(models.Model):
    
    uuid = models.UUIDField(
        _("This is message's ID"),
        primary_key=True,
        editable=False,
        default=uuid4,
        null=False,
        blank=False,
        unique=True
    )
    
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        models.DO_NOTHING,                           
    )
    
    recipent = models.ForeignKey(
        AUTH_USER_MODEL,
        models.DO_NOTHING
    )
    
    text = models.TextField(
        max_length=10000,
        null=False,
        blank=False,
        help_text='Write your message',
    )
    
    date_created = models.DateTimeField(
        _("When it was created"),
        auto_now_add=False
    )
    
    date_changed = models.DateTimeField(
        _("When changed"), 
        auto_now=False,
    )
    
    is_deleted = models.BooleanField(
        _("Is deleted?"),
        default=False,
    )
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-date_created']
        
    def get_all_user_messages(self):
        return Message.objects.filter(author=self.author)
    
    @property
    def is_deleted(self):
        return self.is_deleted
    
    @is_deleted.setter
    def is_deleted(self, value):
        self.is_deleted = value