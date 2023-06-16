from django.contrib import admin
from store.models import *

# Register your models here.

class OrderItemsTublerinline(admin.TabularInline):
    model=OrderItems

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemsTublerinline]
    list_display=['firstname','phone','email','payment_id','paid','date']
    search_fields=['firstname','email','payment_id']

class ImagesTublerinline(admin.TabularInline):
    model=Images

class TagsTublerinline(admin.TabularInline):
    model=Tags

class ProductAdmin(admin.ModelAdmin):
    inlines=[ImagesTublerinline,TagsTublerinline]



admin.site.register(Images)
admin.site.register(Tags)

admin.site.register(Categories)
admin.site.register(Brand)

admin.site.register(Contact_us)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItems)