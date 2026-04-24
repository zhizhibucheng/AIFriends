from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken


class EncryptedCharField(models.CharField):
    description = "基于 AES 的透明加密字符字段"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def fernet(self):
        # 从 settings 中读取我们在第一步配置好的密钥
        return Fernet(settings.ENCRYPTION_KEY)

    def get_prep_value(self, value):
        """存入数据库前自动调用（执行加密）"""
        value = super().get_prep_value(value)
        if value is None or value == '':
            return value

        # Fernet 是极高安全级别的算法，哪怕明文相同，每次生成的密文也都不一样！
        encrypted_bytes = self.fernet.encrypt(value.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')

    def from_db_value(self, value, expression, connection):
        """从数据库读取时自动调用（执行解密）"""
        if value is None or value == '':
            return value

        try:
            decrypted_bytes = self.fernet.decrypt(value.encode('utf-8'))
            return decrypted_bytes.decode('utf-8')
        except InvalidToken:
            # 【神仙级兼容逻辑】：如果你数据库里还有之前测试用的“明文”身份证，
            # 这里解密会报错，我们捕获错误并直接原样返回明文。
            # 这样保证即使不清洗历史数据，系统也绝对不会崩溃！
            return value

    def to_python(self, value):
        if value is None or value == '':
            return value
        return value