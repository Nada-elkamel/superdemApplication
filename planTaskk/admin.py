from django.contrib import admin
from planTaskk.models import UserProfile
from planTaskk.models import  Todo
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(UserProfile)
admin.site.register(Todo)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def save_model(self, request, obj, form, change):
        super(CustomUserAdmin, self).save_model(request, obj, form, change)
        # Create a UserProfile instance for the newly created User
        UserProfile.objects.get_or_create(user=obj)

# Register the User model with the custom admin class
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
