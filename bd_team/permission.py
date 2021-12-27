from django.contrib.auth.models import Permission
from models import *
from django.contrib.contenttypes.models import ContentType

class CouthPermission():
    content_type = ContentType.objects.get_for_model(Player)
    permission = Permission.objects.create(
        codename='can_publish',
        name='Can Publish Player',
        content_type=content_type,
    )