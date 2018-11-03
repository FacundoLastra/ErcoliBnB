from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Prop, ReservationDate, City

admin.site.site_header = "Ercolibnb: admin page"

class ReservationDateInline(admin.TabularInline):
    model = ReservationDate
    exclude = ['reservation']
    fk_name = 'prop'
    max_num = 7


class AdminProp(admin.ModelAdmin):
    inlines = [ReservationDateInline, ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(AdminProp, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


admin.site.register(City)
admin.site.register(Prop, AdminProp)

admin.site.unregister(Group)
