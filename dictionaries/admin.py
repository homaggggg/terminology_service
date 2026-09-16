from django.contrib import admin
from django.utils import timezone
from .models import Dictionary, DictionaryVersion, DictionaryElement

# Register your models here.

class DictionaryVersionInline(admin.TabularInline):
    model = DictionaryVersion
    extra = 1 
    fields = ('version', 'start_date')


class DictionaryElementInline(admin.TabularInline):
    model = DictionaryElement
    extra = 1 
    fields = ('code', 'value')


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'get_current_version', 'get_current_version_date')
    list_display_links = ('id', 'code', 'name')
    fields = ('code', 'name', 'description')
    inlines = [DictionaryVersionInline]

    def _get_latest_version(self, obj):
        return obj.versions.filter(
            start_date__lte=timezone.now().date()
        ).order_by('-start_date').first()

    @admin.display(description="Текущая версия")
    def get_current_version(self, obj):
        latest = self._get_latest_version(obj)
        return latest.version if latest else "—"

    @admin.display(description="Дата начала действия версии")
    def get_current_version_date(self, obj):
        latest = self._get_latest_version(obj)
        return latest.start_date.strftime('%d.%m.%Y') if latest and latest.start_date else "—"


@admin.register(DictionaryVersion)
class DictionaryVersionAdmin(admin.ModelAdmin):
    list_display = ('get_dict_code', 'get_dict_name', 'version', 'start_date')
    list_display_links = ('version',)
    fields = ('dictionary', 'version', 'start_date')
    inlines = [DictionaryElementInline]
    list_filter = ('dictionary', 'start_date')

    @admin.display(description="Код справочника", ordering="dictionary__code")
    def get_dict_code(self, obj):
        return obj.dictionary.code

    @admin.display(description="Наименование справочника", ordering="dictionary__name")
    def get_dict_name(self, obj):
        return obj.dictionary.name


@admin.register(DictionaryElement)
class DictionaryElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'code', 'value')
    list_display_links = ('id', 'code')
    fields = ('version', 'code', 'value')
    list_filter = ('version__dictionary', 'version')