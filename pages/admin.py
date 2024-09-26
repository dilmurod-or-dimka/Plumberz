from django.contrib import admin

from .models import Service, ServicesImage, Staff, StaffImage


class ServicesImageInline(admin.TabularInline):
    model = ServicesImage
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', "slug")
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServicesImageInline]

class StaffImageInline(admin.TabularInline):
    model = StaffImage
    extra = 1

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("full_name", "designation")
    list_display_links = ("full_name", "designation")
    inlines = [StaffImageInline]
