from django.contrib import admin
from web.models.user import UserProfile
from web.models.character import Character, Voice
from web.models.friend import Friend, Message, SystemPrompt


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 1. 列表页展示：使用脱敏后的函数名代替原字段名
    list_display = ('user', 'get_masked_name', 'get_masked_id', 'is_verified', 'is_minor', 'create_time')

    # 2. 搜索功能：依然保留通过原字段搜索的能力（后台会自动解密后比对，或者你也可以改为通过 id_card_hash 搜索）
    search_fields = ('user__username', 'real_name', 'id_card_number')

    # 3. 筛选功能
    list_filter = ('is_verified', 'is_minor')

    # 4. 详情页安全配置：
    # 将敏感信息设为只读，并展示脱敏后的内容
    readonly_fields = (
    'real_name_display', 'id_card_display', 'id_card_hash', 'birth_date', 'create_time', 'update_time')

    # 从编辑表单中彻底移除明文字段，防止管理员查看到解密后的原文或手动篡改
    exclude = ('real_name', 'id_card_number')

    # --- 脱敏逻辑方法 ---

    def real_name_display(self, obj):
        if not obj.real_name: return "未实名"
        name = obj.real_name
        # 脱敏规则：只显示姓，名用星号代替
        return name[0] + '*' * (len(name) - 1)

    real_name_display.short_description = "真实姓名 (已加密存储)"

    def id_card_display(self, obj):
        if not obj.id_card_number: return "未实名"
        id_card = obj.id_card_number
        # 脱敏规则：保留前6位和后4位，中间8位打码
        return id_card[:6] + '********' + id_card[-4:]

    id_card_display.short_description = "身份证号 (已加密存储)"

    # 列表页调用的脱敏包装
    def get_masked_name(self, obj):
        return self.real_name_display(obj)

    get_masked_name.short_description = "姓名"

    def get_masked_id(self, obj):
        return self.id_card_display(obj)

    get_masked_id.short_description = "身份证"


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'voice')


admin.site.register(Voice)


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ('me', 'character',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('friend',)


admin.site.register(SystemPrompt)