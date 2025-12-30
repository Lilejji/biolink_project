from django.contrib import admin
from .models import BioProfile, Link

class LinkInline(admin.TabularInline):
    model = Link
    extra = 1  # Shows one empty extra row by default
    fields = ('title', 'url', 'order')

@admin.register(BioProfile)
class BioProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'get_theme', 'bio') # Added 'get_theme'
    search_fields = ('user__username', 'slug')
    inlines = [LinkInline]

    def get_theme(self, obj):
        return obj.get_theme_display()
    get_theme.short_description = 'Theme'
    
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'order')
    list_filter = ('profile',)