from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    inlines = [CartItemInline]
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at', 'total_price')
    list_filter = ('created_at',)
    search_fields = ('cart__user__username', 'product__name')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'