from .models import Tag


def tag_cloud(request):
    return {'all_tags': Tag.objects.all()}
