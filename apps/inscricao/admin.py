from django.contrib import admin
from .models import Inscricao, Certificado, RequerimentoAmpliacao,Concurso, InformacoesAcademicas
# Register your models here.

admin.site.register(Inscricao)
admin.site.register(Certificado)
admin.site.register(RequerimentoAmpliacao)
admin.site.register(Concurso)
admin.site.register(InformacoesAcademicas)
