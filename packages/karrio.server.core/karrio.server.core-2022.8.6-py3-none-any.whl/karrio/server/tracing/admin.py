from django.contrib import admin
from karrio.server.tracing import models


class TracingRecordAdmin(admin.ModelAdmin):
    readonly_fields = [
        f.name
        for f in models.TracingRecord._meta.get_fields()
        if f.name not in ["org", "link"]
    ]

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.filter(id__in=models.TracingRecord.access_by(request.user))

    def has_add_permission(self, request) -> bool:
        return False


admin.site.register(models.TracingRecord, TracingRecordAdmin)
