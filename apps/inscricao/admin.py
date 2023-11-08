from django.contrib import admin

from .models import Inscricao, Certificado, RequerimentoAmpliacao,Concurso, InformacoesAcademicas
# Register your models here.


class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('professor', 'professor_telefone', 'concluido', 'analisado')

    def professor_telefone(self, obj):
        return obj.professor.telefone

    professor_telefone.short_description = 'Telefone do Professor'  # Nome da coluna na lista


admin.site.register(Inscricao, InscricaoAdmin)
admin.site.register(Certificado)
admin.site.register(RequerimentoAmpliacao)
admin.site.register(Concurso)
admin.site.register(InformacoesAcademicas)
