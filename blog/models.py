from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Blog(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')

    # Fields for the Blog model
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, 
    related_name="blogs",  # Plural because it represents a one-to-many relationship
    verbose_name=_("Author")
)
    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.DRAFT, 
        verbose_name=_("Status")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Published at"))
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True, verbose_name=_("Image"))
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Category"))


    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return self.title

    def get_excerpt(self):
        """Method to get a short preview of the blog content."""
        return self.content[:100] + '...' if len(self.content) > 100 else self.content



class Comment(models.Model):
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE, 
        related_name="comments", 
        verbose_name=_("Blog")
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_("Author")
    )
    content = models.TextField(verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"Comment by {self.author} on {self.blog.title}"