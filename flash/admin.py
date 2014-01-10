from django.contrib import admin
from flash.models import CardSet, Question, Test


class CardSetAdmin(admin.ModelAdmin):
 	list_display = ('name', 'user', 'created', 'lastModified', 'visibleTo', 'view', 'password')

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question', 'questionType', 'cardSet', 'created', 'lastModified')

admin.site.register(CardSet, CardSetAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test)