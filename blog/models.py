from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    # Status choices for the post
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # Post attributes
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()

    # Date and time related fields
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Status field with predefined choices
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    class Meta:
        # Order posts by publish date in descending order
        ordering = ('-publish',)

    def __str__(self):
        # Return a human-readable string representation of the post
        return self.title
