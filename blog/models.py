import re
import html
from django.db import models
from django.utils.text import slugify
from django_summernote.fields import SummernoteTextField


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = SummernoteTextField(verbose_name='正文')
    summary = models.TextField(blank=True, verbose_name='摘要')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='封面图')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='标签')
    is_draft = models.BooleanField(default=True, verbose_name='草稿')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def get_summary(self):
        if self.summary:
            return self.summary
        clean = html.unescape(re.sub(r'<[^>]+>', '', self.content))
        return clean[:150].strip()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[self.pk])

    def __str__(self):
        return self.title
