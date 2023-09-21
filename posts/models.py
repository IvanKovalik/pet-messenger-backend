
from django.urls import reverse
from django.db.models import CharField, ForeignKey, TextField, PositiveIntegerField, ImageField, \
    DateTimeField, Model, DO_NOTHING
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
    
from ivangram.settings import AUTH_USER_MODEL


class Post(Model):
    author = ForeignKey(
        AUTH_USER_MODEL,
        DO_NOTHING,
        help_text='This is authors ID'
    )
    name = CharField(max_length=1000, blank=False)
    text = TextField(max_length=25000)
    image = ImageField(upload_to='media/posts_images/', blank=True)

    reading_time = PositiveIntegerField(default=None, null=True, blank=False)
    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    date_changed = DateTimeField(auto_now=True)
    date_post_created = DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def body_to_string(self):
        return self.text

    class Meta:
        ordering = ['-post_order', '-pub_time']
        verbose_name = _('article')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def get_absolute_url(self):
        return reverse('post-page', kwargs={'post_id': self.id})

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])
        
    def liked(self):
        self.liked += 1
        self.save(update_fields=['likes'])

    def next_post(self):
        return Post.objects.filter(id__gt=self.id).order_by('id').first()

    def previous_post(self):
        return Post.objects.filter(id__lt=self.id).first()