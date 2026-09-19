from django.contrib import admin
from shoppingapp.models import section , product ,detailing ,Cart,completeorder ,Wishlist
# Register your models here.

admin.site.register(section)
admin.site.register(product)
admin.site.register(detailing)
admin.site.register(completeorder)
admin.site.register(Wishlist)
class add_admin_view(admin.ModelAdmin):
    list_display= 'user','product'

admin.site.register(Cart,add_admin_view)