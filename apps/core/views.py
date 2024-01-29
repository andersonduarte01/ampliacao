from django.shortcuts import render
from django.views.generic import TemplateView
from .atualizar_mensagens import atualize_ja


# Create your views here.

class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
