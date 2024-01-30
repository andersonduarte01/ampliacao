from django.contrib import admin

from .models import Inscricao, Certificado, RequerimentoAmpliacao, Concurso, InformacoesAcademicas, Resultado, \
    AmpliacaoComplemento, TotalPontos, Experiencia, Documento


# Register your models here.


class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('professor', 'professor_telefone', 'concluido', 'analisado')

    def professor_telefone(self, obj):
        return obj.professor.telefone

    professor_telefone.short_description = 'Telefone do Professor'


admin.site.register(Inscricao, InscricaoAdmin)


class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'curso')


admin.site.register(Certificado, CertificadoAdmin)


admin.site.register(RequerimentoAmpliacao)


class ConcursoAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'realizacao', 'area', 'posse')

    def inscricao(self, obj):
        inscricao = Inscricao.objects.get(concurso=obj)
        return inscricao

    inscricao.short_description = 'nome'


admin.site.register(Concurso, ConcursoAdmin)


class InfoAcadAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'area_formacao', 'especializacao', 'area_especializacao')

    def inscricao(self, obj):
        inscricao = Inscricao.objects.get(informacoes_academicas=obj)
        return inscricao

    inscricao.short_description = 'nome'


admin.site.register(InformacoesAcademicas, InfoAcadAdmin)

admin.site.register(Resultado)
admin.site.register(AmpliacaoComplemento)
admin.site.register(TotalPontos)
admin.site.register(Experiencia)
admin.site.register(Documento)
