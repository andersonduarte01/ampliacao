from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nome', 'is_admin', 'is_active', 'cadastrado_em', 'atualizado_em')
    search_fields = ('email', 'nome')
    readonly_fields = ('cadastrado_em', 'atualizado_em')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('is_admin', 'is_active')}),
        ('Datas Importantes', {'fields': ('cadastrado_em', 'atualizado_em')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'password1', 'password2', 'is_admin', 'is_active')}
        ),
    )

    ordering = ('email',)

admin.site.register(Usuario, UsuarioAdmin)
