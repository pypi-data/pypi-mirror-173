from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import *


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'is_staff', 'is_active',)
    list_filter = ('email', 'first_name', 'last_name',
                   'username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name',
         'last_name', 'username', 'phone', 'created_by', 'modified_by')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         )
    )
    search_fields = ('email', 'first_name', 'last_name', 'username',)
    ordering = ('email',)


class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "left", "right")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product)


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'brand', 'category')
    list_filter = ('category', 'brand')


@admin.register(CartItem)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product_id', 'quantity')
    list_filter = ('product_id', 'cart')


admin.site.register(OtpData)
admin.site.register(Shop)
admin.site.register(ShopPlan)
admin.site.register(Template)
admin.site.register(Address)
admin.site.register(TokenBlacklist)
admin.site.register(Cart)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


admin.site.register(Attribute)
admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(AttributeValue)
admin.site.register(AttributeValueMapping)
admin.site.register(VariantAttributeMapping)


@admin.register(Configuration)
class CustomConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'value')
