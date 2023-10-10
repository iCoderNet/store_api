from django.contrib import admin
from .models import Category, Product, Review, Order, OrderItem, ShippingAddress, Payment, ProductImage
from mptt.admin import DraggableMPTTAdmin

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    # list_display = ('name', 'description')
    # prepopulated_fields = {'slug': ('name',)}
    pass

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'user')
    search_fields = ('product__name', 'user__username')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status',)
    inlines = [OrderItemInline]

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'address', 'city', 'state', 'zip_code', 'created_at')
    list_filter = ('user', 'state')
    search_fields = ('user__username', 'order__id')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'created_at')
    list_filter = ('payment_method',)
    search_fields = ('order__id',)
