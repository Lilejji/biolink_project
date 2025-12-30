from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class BioProfile(models.Model):
    """
    Represents the public page for a user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, max_length=30)
    bio = models.TextField(max_length=150, blank=True, help_text="A short description about yourself.")
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # Theme Choices
    THEME_CHOICES = [
        ('light', 'Light Mode (Default)'),
        ('dark', 'Dark Mode (Night)'),
    ]
    theme = models.CharField(
        max_length=10, 
        choices=THEME_CHOICES, 
        default='light'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"@{self.slug}"

class Link(models.Model):
    """
    Represents a single clickable item on the profile.
    """
    profile = models.ForeignKey(BioProfile, related_name='links', on_delete=models.CASCADE)
    title = models.CharField(max_length=60, help_text="Button text (e.g., 'My Portfolio')")
    url = models.URLField(help_text="The destination URL")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    
    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.title} (@{self.profile.slug})"
       