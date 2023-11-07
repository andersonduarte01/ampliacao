from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('<int:pk>/', views.Comprovante.as_view(), name='related'),
]
