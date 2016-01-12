from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from import_export import resources

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


class SegmentResource(resources.ModelResource):
    class Meta:
        model = Segment


class SegmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'translation', 'reference', 'batch_id']


class RaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'batch_id', 'get_rating_count']

    def get_rating_count(self, rater):
        return Rating.objects.filter(rater_id=rater.id).count()

    get_rating_count.short_description = 'Rated Segments'


admin.site.register(Segment, SegmentAdmin)
admin.site.register(Rater, RaterAdmin)
admin.site.register(Rating, RatingAdmin)
