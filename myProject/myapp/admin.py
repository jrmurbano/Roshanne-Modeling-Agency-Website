from django.contrib import admin
from .models import (
    UserProfile, ModelCategory, Model, 
    ModelBooking, MagazineCategory, Magazine,
    Photoshoot, Runway, Campaign, Customer, Order, OrderItem
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'height', 'measurements', 'created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(ModelCategory)
class ModelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'category', 'gender', 'age', 'is_available')
    list_filter = ('category', 'gender', 'is_available')
    search_fields = ('user_profile__user__username', 'user_profile__user__email')

@admin.register(ModelBooking)
class ModelBookingAdmin(admin.ModelAdmin):
    list_display = ('model', 'event_name', 'event_date', 'status', 'rate')
    list_filter = ('status', 'event_date')
    search_fields = ('model__user_profile__user__username', 'event_name')

@admin.register(MagazineCategory)
class MagazineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'price', 'category', 'created_at')
    search_fields = ('title', 'name', 'description')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)

@admin.register(Photoshoot)
class PhotoshootAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'photographer')
    list_filter = ('date',)
    search_fields = ('title', 'location', 'photographer')

@admin.register(Runway)
class RunwayAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'designer')
    list_filter = ('date',)
    search_fields = ('title', 'location', 'designer')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'client')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'total_amount', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('order_number', 'customer__user__username', 'customer__user__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    ordering = ('-order_date',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'price', 'quantity', 'total_price')
    list_filter = ('item_type',)
    search_fields = ('order__order_number', 'name')
    readonly_fields = ('created_at',)


