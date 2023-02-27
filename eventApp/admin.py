from django.contrib import admin
from .models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
admin.site.register(Event,EventAdmin)
admin.site.register(Location)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Age_restriction)