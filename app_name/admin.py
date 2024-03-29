from django.contrib import admin
from .models import User, Event, Image, PlusOne
from .models import UserAdmin, EventAdmin, PlusOneAdmin
from .models import GroupAdmin, SessionAdmin
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PlusOne, PlusOneAdmin)
admin.site.register(Image)
