from django.contrib import admin
from myapp.models import Item

class ItemAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(Item,ItemAdmin)






