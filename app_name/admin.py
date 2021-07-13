from django.contrib import admin
from .models import User, UserAdmin, GroupAdmin, Alert, AlertAdmin
from django.contrib.auth.models import Group


admin.site.register(User, UserAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
