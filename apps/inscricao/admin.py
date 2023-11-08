from django.contrib import admin

from .models import Inscricao, Certificado, RequerimentoAmpliacao,Concurso, InformacoesAcademicas
# Register your models here.


class InscricaoAdmin(admin.ModelAdmin):
    model = Inscricao
    list_display = ('professor', 'concluido', 'analisado')


admin.site.register(Inscricao, InscricaoAdmin)
admin.site.register(Certificado)
admin.site.register(RequerimentoAmpliacao)
admin.site.register(Concurso)
admin.site.register(InformacoesAcademicas)
