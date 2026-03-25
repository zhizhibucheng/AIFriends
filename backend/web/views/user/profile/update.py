from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.user import UserProfile
from web.views.utils.photo import remove_old_photo


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            username = request.data.get('username')
            profile = request.data.get('profile')
            photo = request.FILES.get('photo')
            app_background = request.FILES.get('app_background')
            clear_app_background = request.data.get('clear_app_background')

            # 只有当传了 username 时才去更新和校验
            if username is not None:
                username = username.strip()
                if not username:
                    return Response({
                        'result': '用户名不能为空'
                    })
                if username != user.username and User.objects.filter(username=username).exists():
                    return Response({
                        'result': ' 用户名已存在'
                    })
                user.username = username

            # 只有当传了 profile 时才去更新和校验
            if profile is not None:
                profile = profile.strip()[:500]
                if not profile:
                    return Response({
                        'result': '简介不能为空'
                    })
                user_profile.profile = profile

            if photo:
                remove_old_photo(user_profile.photo)
                user_profile.photo = photo

            # 2. 再处理背景（🚨 注意：这里和上面的 if photo 必须是对齐的！）
            if str(clear_app_background).lower() == 'true':
                # 如果收到清除信号，删掉旧的自定义图（如果是 default 就不删）
                if user_profile.app_background and 'default.png' not in user_profile.app_background.name:
                    try:
                        remove_old_photo(user_profile.app_background)
                    except:
                        pass
                # 将数据库字段恢复为默认值
                user_profile.app_background = 'user/app_backgrounds/default.png'
            elif app_background:
                # 原本的上传新背景逻辑
                if user_profile.app_background and 'default.png' not in user_profile.app_background.name:
                    try:
                        remove_old_photo(user_profile.app_background)
                    except:
                        pass
                user_profile.app_background = app_background
            user_profile.update_time = now()

            # user_profile.profile = profile
            user_profile.update_time = now()
            user_profile.save()
            # user.username = username
            user.save()
            return Response({
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'profile': user_profile.profile,
                'photo': user_profile.photo.url,
                'app_background': user_profile.app_background.url,
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })