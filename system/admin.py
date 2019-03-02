from django.contrib import admin
from system.models import Users
from django.contrib.auth.admin import UserAdmin


class UsersAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('基本信息', {'fields': ('first_name', 'last_name', 'email')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('登录时间', {'fields': ('last_login', 'date_joined')}),
        ('其他信息', {'fields': (
            'position', 'avatar', 'mobile',)}),
    )

    @classmethod
    def show_group(self, obj):
        return [i.name for i in obj.groups.all()]

    @classmethod
    def show_user_permissions(self, obj):
        return [i.name for i in obj.user_permissions.all()]

    list_display = ('username', 'show_group', 'show_user_permissions')
    list_display_links = ('username',)
    search_fields = ('username',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(Users, UsersAdmin)
admin.site.site_header = '海豹管理后台'
admin.site.site_title = admin.site.site_header
