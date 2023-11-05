from django.urls import path
from . import views

app_name = 'inscricao'

urlpatterns = [
    path('', views.InscricaoView.as_view(), name='inscrever'),
    path('informacoes_academicas/', views.InfoAcademicas.as_view(), name='academica'),
    path('adicionar/informacoes_academicas/', views.InfoAcademicasUp.as_view(), name='up_academica'),
    path('concurso/', views.Concurso.as_view(), name='concurso'),
    path('adicionar/concurso/', views.ConcursoDetail.as_view(), name='detail_concurso'),
    path('certificados/', views.certificadoTeste, name='certificado'),
    path('adicionar/certificados/', views.certificadoUp, name='up_certificado'),
    path('requerimento/', views.requerimentoTeste, name='requerimento'),
    path('adicionar/requerimento/', views.requerimentoUp, name='up_requerimento'),
    path('<int:pk>/termo_de_compromisso/', views.Termo.as_view(), name='termo'),
    path('adicionar/<int:pk>/termo_de_compromisso/', views.TermoUP.as_view(), name='up_termo'),
    ## analises
    path('<int:pk>/resultado_da_analise', views.AnalisarIncricao.as_view(), name='analisar')

]
