from django.contrib import admin
from .models import Beats

class BeatsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'score', 'artist', 'genre', 'release_date', 'price')

    # Fields to filter the list by
    list_filter = ('genre', 'release_date', 'artist', 'score')

    # Fields to search by
    search_fields = ('title', 'artist__username', 'genre')


    # Fields to be edited inline
    fieldsets = (
        (None, {
            'fields': ('title', 'artist', 'genre', 'duration', 'release_date', 'price', 'BPM', 'description', 'views')
        }),
        ('Media', {
            'fields': ('cover_image', 'audio_file')
        }),
    )


admin.site.register(Beats, BeatsAdmin)
