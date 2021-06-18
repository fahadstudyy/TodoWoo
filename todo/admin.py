from django.contrib import admin
from .models import todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields= ('created', )

admin.site.register(todo, TodoAdmin)

