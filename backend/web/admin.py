from django.contrib import admin

from web.models.user import UserProfile
from web.models.character import Character, Voice
from web.models.friend import Friend, Message, SystemPrompt


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'real_name', 'is_verified', 'is_minor', 'create_time')

    # 允许在后台通过用户名、真实姓名和身份证号搜索用户
    search_fields = ('user__username', 'real_name', 'id_card_number')

    # 在后台右侧增加筛选器，方便一键筛选未成年用户或未实名用户
    list_filter = ('is_verified', 'is_minor')


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
