from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile
# ====== 新增脱敏工具函数 ======
def mask_name(name):
    if not name: return ""
    if len(name) <= 2:
        return name[0] + '*'
    else:
        return name[0] + '*' * (len(name) - 2) + name[-1]

def mask_id_card(id_card):
    if not id_card or len(id_card) != 18: return ""
    return id_card[:6] + '********' + id_card[-4:]
# ==============================

class GetUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)

            # 只有已实名用户，才进行脱敏提取
            masked_name = mask_name(user_profile.real_name) if user_profile.is_verified else ""
            masked_id_card = mask_id_card(user_profile.id_card_number) if user_profile.is_verified else ""

            return Response({
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'photo': user_profile.photo.url,
                'profile': user_profile.profile,
                'app_background': user_profile.app_background.url,
                'is_verified': user_profile.is_verified,
                'is_minor': user_profile.is_minor,
                'real_name_masked': masked_name,
                'id_card_masked': masked_id_card,
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })