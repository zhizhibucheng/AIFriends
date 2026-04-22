from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character
from web.models.friend import Friend
from web.models.user import UserProfile


class GetOrCreateFriendView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            character_id = request.data['character_id']
            user = request.user

            # 新增：提前验证该角色是否存在及是否可见（脏数据拦截）
            try:
                check_character = Character.objects.get(id=character_id)
            except Character.DoesNotExist:
                return Response({'result': '该角色不存在'}, status=404)

            if not check_character.is_public and check_character.author.user != user:
                # 返回特定的业务错误，配合 HTTP 403 状态码供前端轻易捕获
                return Response({'result': '该角色已不可见，请刷新'}, status=403)



            user_profile = UserProfile.objects.get(user=user)

            if not user_profile.is_verified:
                # 状态码使用 403，配合前端 Character.vue 里的 catch 逻辑
                return Response({'result': '为了您的体验，请先完成实名认证'}, status=403)

            if user_profile.is_minor:
                # 状态码使用 403，前端会自动弹窗倒计时提示
                return Response({'result': '根据相关法规，未成年人无法使用AI互动聊天服务'}, status=403)

            friends = Friend.objects.filter(character_id=character_id,me=user_profile)
            if friends.exists():
                friend = friends.first()
            else:
                friend = Friend.objects.create(character_id=character_id, me=user_profile)
            character = friend.character
            author = character.author
            return Response({
                'result': 'success',
                'friend': {
                    'id': friend.id,
                    'character': {
                        'id': character.id,
                        'name': character.name,
                        'profile': character.profile,
                        'photo': character.photo.url,
                        'background_image': character.background_image.url,
                        'author': {
                            'user_id': author.user_id,
                            'username': author.user.username,
                            'photo': author.photo.url,
                        }
                    }
                }
            })
        except:
            return Response({
                'result': '系统异常，请稍后重试'
            })