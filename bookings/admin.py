from django.contrib import admin
from .models import Provider, Availability, Service, Notification, Booking


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'location', 'rating', 'created_at']
    list_filter = ['service_type', 'location']
    search_fields = ['name', 'description']


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['provider', 'service', 'date', 'start_time', 'end_time', 'is_available']
    list_filter = ['is_available', 'date', 'provider']
    search_fields = ['provider__username']
    date_hierarchy = 'date'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'category', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'provider__username']
    date_hierarchy = 'created_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['service', 'customer', 'provider', 'date', 'start_time', 'status', 'price', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['customer__username', 'provider__username', 'service__name']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} booking(s) marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_as_completed.short_description = "Mark selected bookings as completed"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"
