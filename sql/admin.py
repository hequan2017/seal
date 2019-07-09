from django.contrib import admin
from sql.models import database


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'address', 'port', 'ctime', 'password', "get_password")


class SqlPermAdmin(admin.ModelAdmin):

    @classmethod
    def show_approver(self, obj):
        return [i.username for i in obj.approver.all()]

    search_fields = ['group']
    list_display = ('group', "show_approver", "ddl", "dml", "select")
    filter_horizontal = ('approver', "ddl_data", "dml_data", "select_data")


class SqlUserAdmin(admin.ModelAdmin):

    @classmethod
    def show_perm(self, obj):
        return [i.group for i in obj.perm.all()]

    list_display = ('user', 'show_perm')
    search_fields = ['user']
    filter_horizontal = ('perm',)


admin.site.register(database, DatabaseAdmin)
