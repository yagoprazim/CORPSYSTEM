from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from api.models.client import Client
from api.models.vendor import Vendor
from api.models.product import ProductGroup, Product
from api.models.sale import Sale, SaleItem

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'email', 'phone', 'registered_dttm')
    search_fields = ('name', 'cpf')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'credential_code', 'email', 'phone', 'joined_dttm')
    search_fields = ('name', 'credential_code')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'group')
    search_fields = ('name', 'group__name')

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    readonly_fields = ('total_price',)
    extra = 1

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ('client', 'vendor', 'date', 'total_amount')
    readonly_fields = ('client', 'vendor', 'total_amount',)
    search_fields = ('client__name', 'vendor__name')

    def has_add_permission(self, request):
        return False

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ProductGroup)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)


