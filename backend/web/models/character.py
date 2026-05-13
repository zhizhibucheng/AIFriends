import uuid

from django.db import models
from django.utils.timezone import now, localtime

from web.models.user import UserProfile


def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/photo/{instance.author.user_id}_{filename}'

def background_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'character/background_image/{instance.author.user_id}_{filename}'

class Voice(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    voice_id = models.CharField(max_length=100)
    created_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} - {self.voice_id} - {localtime(self.created_time).strftime('%Y-%m-%d %H:%M:%S')}"


class Character(models.Model):
    # --- 新增：3D实体形态选项 ---
    AVATAR_CHOICES = (
        ('none', '无'),
        ('male', '男性'),
        ('female', '女性'),
        ('dog', '小狗'),
        ('cat', '小猫'),
    )

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=photo_upload_to)
    voice = models.ForeignKey(Voice, default=None, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.TextField(max_length=100000)
    background_image = models.ImageField(upload_to=background_image_upload_to)
    is_public = models.BooleanField(default=True, verbose_name="是否公开")
    avatar_type = models.CharField(max_length=20, choices=AVATAR_CHOICES, default='none', verbose_name="3D模型类型")

    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.author.user.username} - {'公开' if self.is_public else '私密'} - {self.name} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}"
