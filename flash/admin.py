from django.contrib import admin
from flash.models import CardSet, Question, Test




admin.site.register(CardSet)
admin.site.register(Question)
admin.site.register(Test)

# class PageAdmin(admin.ModelAdmin):
# 	list_display = ('title', 'category', 'url')
# admin.site.register(Page, PageAdmin)