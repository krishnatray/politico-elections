from django.contrib import admin

from geography.models import (Division, DivisionLevel, Geography,
                              IntersectRelationship)


class IntersectRelationshipInline(admin.StackedInline):
    model = IntersectRelationship
    fk_name = 'from_division'
    extra = 0


class DivisionAdmin(admin.ModelAdmin):
    inlines = (IntersectRelationshipInline,)
    list_display = ('label', 'level', 'code')
    list_filter = ('level',)
    search_fields = ('code',)
    readonly_fields = ('parent', 'uid',)


class GeographyAdmin(admin.ModelAdmin):
    list_display = ('division', 'map_level', 'small_preview')
    search_fields = ('division',)
    readonly_fields = ('file_size', 'large_preview',)

    fieldsets = (
        (None, {
            'fields': ('division', 'subdivision_level',)
        }),
        ('Geo data', {
            'fields': (
                'topojson', 'simplification',
                'file_size', 'large_preview',)
        }),
        ('In effect', {
            'fields': ('effective', 'effective_start', 'effective_end',)
        }),
    )

    def map_level(self, obj):
        return obj.subdivision_level.name


admin.site.register(DivisionLevel)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Geography, GeographyAdmin)
