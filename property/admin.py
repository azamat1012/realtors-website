from django.contrib import admin
from property.models import Flat, Complaint, Owner

class OwnerInline(admin.TabularInline):
    model = Owner.flat.through  
    raw_id_fields = ['owner']
    extra = 0

@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'address', 'owner__full_name']
    readonly_fields = ['created_at']
    list_display = ['address', 'price', 'is_new_building',
                    'construction_year', ]
    list_editable = ['is_new_building']
    list_filter = ['is_new_building', 'rooms_number', 'has_balcony']
    inlines = [OwnerInline]
    raw_id_fields = ['likes', 'owners']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'flat', 'complaint_text']
    raw_id_fields = ['flat']
    search_fields = ['user__username', 'complaint_text']

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'normalized_phone')
    fields = ('full_name', 'phone_number', 'normalized_phone', 'flat') 
    search_fields = ['full_name', 'phone_number']
    raw_id_fields = ['flat']  