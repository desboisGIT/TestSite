from django.contrib import admin
from .models import Beats

class BeatsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title','id', 'artist', 'genre', 'release_date', 'price')
    
    # Fields to filter the list by
    list_filter = ('genre', 'release_date', 'artist')
    
    # Fields to search by
    search_fields = ('title', 'artist__username', 'genre')
    
    # Fields to be edited inline
    fieldsets = (
        (None, {
            'fields': ('title', 'artist', 'genre', 'duration', 'release_date', 'price', 'BPM','description','views')
        }),
        ('Media', {
            'fields': ('cover_image', 'audio_file')
        }),
    )
    
    # Adding inline display of cover image
    readonly_fields = ('cover_image_preview',)

    def cover_image_preview(self, obj):
        return obj.cover_image.url if obj.cover_image else 'No Image'
    cover_image_preview.short_description = 'Cover Image'
    cover_image_preview.allow_tags = True

# Register the model and the admin customization
admin.site.register(Beats, BeatsAdmin)
