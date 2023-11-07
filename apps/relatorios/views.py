import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from ..inscricao.models import Inscricao
from .conversor import html_to_pdf2


class Comprovante(View):
    def get(self, request, *args, **kwargs):
        inscricao = get_object_or_404(Inscricao, pk=self.kwargs['pk'])
        nome_arquivo = f'{inscricao.id}'
        open('templates/temp.html', "w", encoding='UTF-8').write(render_to_string
                                                                 ('relatorios/comprovate.html', {'inscricao': inscricao}))

        #open(f'/home/anderson/projeto/gabarito/templates/{nome_arquivo}.html', "w", encoding='UTF-8').write(render_to_string
         #                                                                ('relatorios/relatorio_sala.html', {'data': data, 'gabaritos': gabaritos, 'questoes': questoes}))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf2('temp.html')
        #pdf = html_to_pdf2(f'/home/anderson/projeto/gabarito/templates/{nome_arquivo}.html')


        #os.remove(f'/home/anderson/projeto/gabarito/templates/{nome_arquivo}.html')

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')




