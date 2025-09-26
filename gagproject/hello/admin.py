from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Users)
admin.site.register(roles)
admin.site.register(donations)
admin.site.register(subscriptions)
admin.site.register(level)
admin.site.register(streams)
admin.site.register(categories)