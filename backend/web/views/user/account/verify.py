import re
from datetime import datetime
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from web.models.user import UserProfile
import hashlib

class VerifyUserView(APIView):
    # 必须登录后才能进行实名认证
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        real_name = request.data.get('real_name')
        id_card_number = request.data.get('id_card_number')

        if not real_name or not id_card_number:
            return Response({'error': '真实姓名和身份证号不能为空'}, status=400)

        # 1. 初步校验身份证格式 (中国大陆身份证为18位，最后一位可能是 X/x)
        if not re.match(r'^\d{17}[\dXx]$', id_card_number):
            return Response({'error': '身份证号格式不正确'}, status=400)

        # ================== 核心安全修改：哈希防重 ==================
        # 生成身份证号的不可逆 SHA-256 哈希值
        id_card_hash = hashlib.sha256(id_card_number.encode('utf-8')).hexdigest()

        # 检查该哈希值是否已被其他账号绑定（不比较明文，安全！）
        if UserProfile.objects.filter(id_card_hash=id_card_hash).exclude(user=user).exists():
            return Response({'error': '该身份证已被其他账号实名认证'}, status=400)
        # ==========================================================

        api_url = 'https://eolink.o.apispace.com/identity-two/name_number'  # 替换为服务商提供的真实URL
        app_token = settings.APISPACE_TOKEN

        if not app_token:
            # 如果本地开发环境没配置 AppCode，暂且拦截报错，或者你也可以设为开发环境模拟通过
            return Response({'error': '系统未配置实名认证服务'}, status=500)

        payload = {
            "realname": real_name,
            "idcard": id_card_number
        }

        # 构造 Headers，严格按照 APISpace 的要求
        headers = {
            "X-APISpace-Token": app_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(api_url, data=payload, headers=headers, timeout=5)
            result_data = response.json()

            # 根据 APISpace 示例，外层 code 为 0 表示接口请求成功（成功扣费）
            if str(result_data.get('code')) == '0':
                inner_data = result_data.get('data', {})

                # valid 为 true 或者 incorrect 为 100 表示姓名与身份证一致
                if inner_data.get('valid') is True or inner_data.get('incorrect') == 100:
                    pass  # 一致，跳过报错，继续往下走
                else:
                    # 获取 101(不一致) 或 102(无此号) 的具体描述
                    error_msg = inner_data.get('message', '姓名与身份证号不匹配')
                    return Response({'error': f'认证失败：{error_msg}'}, status=400)
            else:
                # 接口调用失败（例如参数错误、余额不足、Token失效等）
                return Response({'error': result_data.get('message', '实名认证服务异常')}, status=500)

        except requests.exceptions.Timeout:
            return Response({'error': '实名认证服务请求超时，请稍后再试'}, status=504)
        except requests.exceptions.RequestException as e:
            print(f"实名认证API请求异常: {str(e)}")
            return Response({'error': '实名认证服务暂时不可用，请联系客服'}, status=500)

        # 4. 从身份证中提取出生年月日并计算未成年状态
        birth_date_str = id_card_number[6:14]  # 提取 YYYYMMDD
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y%m%d').date()
        except ValueError:
            return Response({'error': '身份证包含无效的出生日期'}, status=400)

        today = datetime.now().date()
        # 计算精确周岁年龄
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        # 核心合规逻辑：判定是否为未成年
        is_minor = age < 18

        # 5. 更新数据库信息
        profile = UserProfile.objects.get(user=user)

        profile.real_name = real_name
        profile.id_card_number = id_card_number
        profile.id_card_hash = id_card_hash  # 存入防重复的哈希值
        profile.is_verified = True
        profile.is_minor = is_minor
        profile.birth_date = birth_date
        profile.save()

        # 返回认证结果及合规状态
        return Response({
            'result': 'success',
            'message': '实名认证成功',
            'is_verified': True,
            'is_minor': is_minor,
            'age': age
        })