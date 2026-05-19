from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# This tells Django: "Take my CustomUser table, and display it in the admin 
# panel using the standard, highly secure UserAdmin layout."
admin.site.register(CustomUser, UserAdmin)