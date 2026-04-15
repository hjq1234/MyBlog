from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = '博客'

    def ready(self):
        # django-summernote 的 bleach 白名单默认没有 img[src]，
        # 导致保存时图片 src 被清除。这里原地修改白名单 dict（原地改可传播到 fields.py）。
        import django_summernote.settings as ds
        ds.ATTRIBUTES['img'] = ['src', 'alt', 'width', 'height', 'style']
        ds.ATTRIBUTES['th'] = ['style', 'colspan', 'rowspan', 'align']
        ds.ATTRIBUTES['td'] = ['style', 'colspan', 'rowspan', 'align']

        # 汉化 django-summernote 的 app 名称和 Attachment 模型名称
        from django.apps import apps
        summernote_app = apps.get_app_config('django_summernote')
        summernote_app.verbose_name = 'Summernote 附件'
        attachment_model = summernote_app.get_model('Attachment')
        attachment_model._meta.verbose_name = '附件'
        attachment_model._meta.verbose_name_plural = '附件'
