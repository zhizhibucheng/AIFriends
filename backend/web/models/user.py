import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, localtime


def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return f'user/photos/{instance.user_id}_{filename}'

def app_background_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'user/app_backgrounds/{instance.user_id}_{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='user/photos/default.png', upload_to=photo_upload_to)
    app_background = models.ImageField(default='user/app_backgrounds/default.png', upload_to=app_background_upload_to,
                                       verbose_name="系统背景")

    profile = models.TextField(default='谢谢你的关注', max_length=500)
    # ================== 新增：实名认证与未成年人保护合规字段 ==================
    real_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="真实姓名")
    id_card_number = models.CharField(max_length=18, unique=True, null=True, blank=True, verbose_name="身份证号")
    is_verified = models.BooleanField(default=False, verbose_name="是否已实名")
    is_minor = models.BooleanField(default=False, verbose_name="是否未成年")
    birth_date = models.DateField(null=True, blank=True, verbose_name="出生日期")
    # ========================================================================
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} - {localtime(self.create_time).strftime("%Y-%m-%d %H:%M:%S")}'
