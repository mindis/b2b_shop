from django.contrib import admin
from .models import ProductClass, Product, ProductVariant, \
                    SaleSum, SaleQuantity, Organisation, \
                    OrderItem, Order, Invoice, SellerOrganisation,\
                    Price

from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

#admin.site.register(ProductVariant)
#admin.site.register(SaleSum)
#admin.site.register(SaleQuantity)
admin.site.register(ProductClass)
#admin.site.register(Product)
admin.site.register(Organisation)
#admin.site.register(OrderItem)
#admin.site.register(Order)
#admin.site.register(Invoice)
admin.site.register(SellerOrganisation)
#admin.site.register(Price)

class PriceInline(SuperInlineModelAdmin, admin.TabularInline):
    model = Price
    extra = 0

class ProductVariantAdmin(SuperModelAdmin):
    inlines = [PriceInline,]
    list_display = ('name', 'slug', 'vendorCode', 'quantity')

class OrderItemInline(SuperInlineModelAdmin, admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderInline(SuperInlineModelAdmin, admin.StackedInline):
    model = Order
    extra = 0
    inlines = [OrderItemInline,]

class InvoiceAdmin(SuperModelAdmin):
    inlines = [OrderInline,]
    list_display = ('pk', 'date', 'seller', 'customer', 'toPay')

class ProductVariantInline(SuperInlineModelAdmin, admin.TabularInline):
    #inlines = [PriceInline,]
    model = ProductVariant
    extra = 0

class ProductAdmin(SuperModelAdmin):
    inlines = [ProductVariantInline,]
    list_display = ('pk', 'name', 'slug')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Invoice, InvoiceAdmin)
