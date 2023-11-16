from django.shortcuts import render
from django.views.generic import TemplateView
from .correcao import corrigirRequerimento


# Create your views here.

class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        corrigirRequerimento()
        return contexto
