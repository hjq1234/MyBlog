import re
from django.db import models
from django.utils.text import slugify
from django_summernote.fields import SummernoteTextField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = SummernoteTextField()
    summary = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    is_draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_summary(self):
        if self.summary:
            return self.summary
        clean = re.sub(r'<[^>]+>', '', self.content)
        return clean[:150].strip()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[self.pk])

    def __str__(self):
        return self.title
