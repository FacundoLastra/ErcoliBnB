from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Prop, ReservationDate, City

admin.site.site_header = "Ercolibnb: admin page"

class ReservationDateInLine(admin.TabularInline):
    model=ReservationDate
    fk_name ='prop'
    min_num = 7

class AdminPropertyInLine(admin.ModelAdmin):
    inlines=[ReservationDateInLine]
    exclude = ['owner']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(AdminPropertyInLine, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

admin.site.register(City)
admin.site.register(Prop, AdminPropertyInLine)

admin.site.unregister(Group)
