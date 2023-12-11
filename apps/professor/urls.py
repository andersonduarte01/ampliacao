from django.urls import path
from . import views

app_name = 'professor'

urlpatterns = [
    path('', views.CadastrarProfessor.as_view(), name='cad_professor'),
    path('atualizar_dados/<int:pk>/', views.AtualizarProfessor.as_view(), name='up_professor'),
    path('detalhes/', views.DetalhesInscricao.as_view(), name='detalhes'),
    ## ADM
    path('painel/', views.PainelAdm.as_view(), name='administrador'),
    ## Tabelas
    path('lista/', views.ProfessoresList.as_view(), name='prof_list'),
    path('lista_inscricoes/', views.InscricoesList.as_view(), name='insc_list'),
    path('inscricoes_pendentes/', views.InscricoesPendentes.as_view(), name='pend_list'),
    path('inscricoes_analisadas/', views.InscricoesAnalisadas.as_view(), name='concl_list'),
    path('inscricoes_incompletas/', views.InscricoesIncompletas.as_view(), name='incompletas_list'),
    path('inscricoes_outros/', views.InscricoesOutros.as_view(), name='outros_list'),
]
