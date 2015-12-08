from django.contrib import admin

from .models import Segment, Rater, Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ('get_segment_translation', 'rating', 'get_email')

    def get_email(self, rating):
        return rating.rater.email

    get_email.short_description = 'Rater'
    get_email.admin_order_field = 'rater__email'

    def get_segment_translation(self, rating):
        return rating.segment.translation

    get_segment_translation.short_description = 'Translation'
    get_segment_translation.admin_order_field = 'segment__pk'


class SegmentAdmin(admin.ModelAdmin):
    list_display = ['translation', 'reference']


class RaterAdmin(admin.ModelAdmin):
    list_display = ['email']


admin.site.register(Segment, SegmentAdmin)
admin.site.register(Rater, RaterAdmin)
admin.site.register(Rating, RatingAdmin)
