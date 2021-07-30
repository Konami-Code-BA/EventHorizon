from django.contrib import admin
from .models import User, UserAdmin, GroupAdmin, Alert, AlertAdmin, SessionAdmin, Event, EventAdmin
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session


admin.site.register(User, UserAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Event, EventAdmin)
