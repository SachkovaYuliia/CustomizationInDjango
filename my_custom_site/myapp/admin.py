from django.contrib import admin
from .models import CustomModel, Category

@admin.register(CustomModel)
class CustomModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'word_count', 'character_count')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')
    actions = ['mark_as_processed']

    def word_count(self, obj):
        return obj.calculate_statistics()['words']

    word_count.short_description = 'Number of Words'

    def character_count(self, obj):
        return obj.calculate_statistics()['characters']

    character_count.short_description = 'Number of Characters'

    def mark_as_processed(self, request, queryset):
        queryset.update(content="This item has been processed")
        self.message_user(request, "Selected items have been marked as processed.")
    mark_as_processed.short_description = "Mark selected as processed"

class CustomModelInline(admin.TabularInline):
    model = CustomModel
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [CustomModelInline]

admin.site.register(Category, CategoryAdmin)
