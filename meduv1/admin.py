from django.contrib import admin
from .models import University, CustomUser,  Application, Location

# Register your models here.
admin.site.register(University)
admin.site.register(CustomUser)
admin.site.register(Application)
admin.site.register(Location)