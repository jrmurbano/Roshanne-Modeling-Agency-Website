from django.contrib import admin
from .models import (
    Category, Post, UserProfile, ModelCategory, Model, 
    ModelBooking, MagazineCategory, Magazine, MagazineOrder,
    Photoshoot, Runway, Campaign, Customer
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

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

@admin.register(MagazineOrder)
class MagazineOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'magazine', 'customer', 'quantity', 'total_price', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('magazine__title', 'customer__user__username', 'customer_name', 'customer_email')

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


