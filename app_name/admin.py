from django.contrib import admin
from .models import User, UserAdmin, GroupAdmin
from django.contrib.auth.models import Group


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
