from django.contrib import admin
from .models import Hobby, Location, Workshop, Review, WorkshopApply

admin.site.register(Hobby)
admin.site.register(Location)
# admin.site.register(Workshop)
admin.site.register(Review)


# ManyToMany 중간테이블 화면 출력
class WorkshopApplyInline(admin.TabularInline):
    model = WorkshopApply
    extra = 2 # how many rows to show

class WorkshopAdmin(admin.ModelAdmin):
    inlines = [
        WorkshopApplyInline,
    ]

admin.site.register(Workshop, WorkshopAdmin)