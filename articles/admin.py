from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        mains_list = []
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            #form.cleaned_data
            if form.cleaned_data != {}:
                #print(form.cleaned_data['tag'], form.cleaned_data['is_main'])
                if form.cleaned_data['is_main'] == True:
                    mains_list.append(form.cleaned_data['is_main'])
            if mains_list.count(True) != 1:
                # вызовом исключения ValidationError можно указать админке о наличие ошибки
                # таким образом объект не будет сохранен,
                # а пользователю выведется соответствующее сообщение об ошибке
                raise ValidationError('Должен быть один основной раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода
class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0
@admin.register(Tag)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image']
    inlines = [ScopeInline,]