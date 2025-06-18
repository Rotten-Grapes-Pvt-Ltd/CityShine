from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import IssueType, Issue

admin.site.register(IssueType)

@admin.register(Issue)
class IssueAdmin(GISModelAdmin):
    list_display = ('title', 'issue_type', 'user', 'status', 'created_at')
    list_filter = ('status', 'issue_type', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    # Set the map to use EPSG:4326 projection
    map_srid = 4326
    default_lon = 78.9629
    default_lat = 20.5937
    default_zoom = 5