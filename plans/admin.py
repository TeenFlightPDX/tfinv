from django.contrib import admin

from .models import Kit, Section, Page, Step

admin.site.register(Kit)
admin.site.register(Page)


class StepInLine(admin.StackedInline):
    model = Step
    classes = ['collapse']


class PageInLine(admin.TabularInline):
    def number_of_steps(self):
        return self.getSteps().count()

    model = Page
    extra = 0
    ordering = ('page_number',)
    fields = ('page_number', number_of_steps, 'confirmed')
    readonly_fields = ('page_number', number_of_steps)
    show_change_link = True


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_number', 'kit', 'name', 'confirmed')

    inlines = [
        PageInLine
    ]


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'page_number', 'step_number', 'confirmed')
    list_filter = ('page__section',)

    def page_number(self, obj):
        return obj.page.page_number

    def section_name(self, obj):
        return obj.page.section
