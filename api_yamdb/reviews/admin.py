from django.contrib import admin
from .models import User
from .models import Categories, Genres, Titles, Reviews, Comments

class UserAdmin(admin.ModelAdmin):
    """Конфигурируем пользовательскую модель в админке."""
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )
    list_editable = (
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    empty_value_display = ('-пусто-')


admin.site.register(User, UserAdmin)
admin.site.register(Categories) 
admin.site.register(Genres) 
admin.site.register(Titles) 
admin.site.register(Reviews)
admin.site.register(Comments)