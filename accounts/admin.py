from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('user_type', 'phone_number', 'city', 'bio', 'service_type', 'kvk_number', 'birthday', 'address')


# Extend the User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'userprofile__user_type')

    def get_user_type(self, obj):
        try:
            return obj.userprofile.get_user_type_display()
        except:
            return '-'
    get_user_type.short_description = 'Account Type'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Separate admin for UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone_number', 'city', 'service_type']
    list_filter = ['user_type', 'city', 'service_type']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_type')
        }),
        ('Contact Information', {
            'fields': ('phone_number',)
        }),
        ('Provider Information', {
            'fields': ('city', 'bio', 'service_type', 'kvk_number'),
            'description': 'Only for service providers'
        }),
        ('Customer Information', {
            'fields': ('birthday', 'address'),
            'description': 'Only for customers'
        }),
    )
