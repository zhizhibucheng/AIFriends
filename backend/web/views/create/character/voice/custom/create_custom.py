# 这个接口将负责：接收前端传来的录音 -> 保存到服务器 -> 获取外网URL -> 调用复刻API -> 存入数据库。

import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.files.storage import default_storage

from web.models.character import Voice

from web.views.create.character.voice.custom.create_voice import create_voice


class CreateCustomVoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({
                'result': 'failed',
                'message': '未找到音频文件'
            })

        user_profile = request.user.userprofile

        # 保存音频文件到本地 media 目录
        ext = audio_file.name.split('.')[-1] if '.' in audio_file.name else 'webm'
        filename = f"user_voices/{user_profile.user_id}_{uuid.uuid4().hex[:10]}.{ext}"

        # 使用 Django 的文件系统保存文件
        saved_path = default_storage.save(filename, audio_file)

        # 拼接可通过公网访问的 URL
        # request.build_absolute_uri 可以动态获取当前服务器域名
        # 如果你部署在服务器上且使用了 Nginx 反向代理，导致获取到的是 http，建议直接写死你的域名，例如：
        audio_url = f"https://zhizhibuchengai.com.cn/media/{saved_path}"

        # 调用阿里云接口复刻声音
        prefix = uuid.uuid4().hex[:10]
        try:
            # 调用已有的复刻方法
            res = create_voice(audio_url, prefix)

            # 提取阿里云返回的 voice_id
            aliyun_voice_id = res.get('output', {}).get('voice_id')

            if not aliyun_voice_id:
                return Response({'result': 'failed', 'message': '语音复刻失败，未获取到音色ID', 'detail': res})

        except Exception as e:
            return Response({'result': 'failed', 'message': f'调用复刻接口异常: {str(e)}'})

        #  保存到数据库 (关联当前用户，并设置为不公开)
        voice_name = f"{request.user.username} 的专属音色"
        new_voice = Voice.objects.create(
            name=voice_name,
            voice_id=aliyun_voice_id,
            author=user_profile,
            is_public=False  # 设置为私有音色
        )

        return Response({
            'result': 'success',
            'voice_id': new_voice.id,  # 返回我们自己数据库的主键 ID 给前端
            'message': '专属音色生成成功！'
        })