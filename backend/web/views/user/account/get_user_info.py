from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile


class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            return Response({
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'photo': user_profile.photo.url,
                'profile': user_profile.profile,
                'app_background': user_profile.app_background.url,
                'is_verified': user_profile.is_verified,
                'is_minor': user_profile.is_minor,
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })