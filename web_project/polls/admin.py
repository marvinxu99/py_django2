# Custom Admin Page:
# https://docs.djangoproject.com/en/3.0/intro/tutorial07/
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """
    Using TabularInline (instead of StackedInline), the related objects 
    are displayed in a more compact, table-based format:
    """
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """
    Replacing admin.site.register(Question) with the fillowing:
    You’ll follow this pattern – create a model admin class,
    then pass it as the second argument to admin.site.register() – any
    time you need to change the admin options for a model.
    """
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None,  {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
