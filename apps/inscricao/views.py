import uuid
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

from .forms import CertificadoForm, RequerimentoForm, ConcursoForm, InscricaoCheck, RequerimentoAmpliacaoCheck, \
    InformacoesCheck, ResultadoForm, ComplementoForm, RecursoForm, ComplementoCheck, PontosForm, ExperienciaForm, \
    PosPontosForm, ResultadoRecursoForm
from .models import Inscricao, InformacoesAcademicas, Concurso, RequerimentoAmpliacao, Certificado, Resultado, \
    AmpliacaoComplemento, TotalPontos, Experiencia, PosTotalPontos, Recurso, ResultadoRecurso
from ..professor.models import Professor
from ..inscricao.decoradores import StaffRequiredMixin
import unicodedata

def generate_random_filename(filename):
    if filename:
        ext = filename.split('.')[-1]  # Obtém a extensão do arquivo original
        random_name = str(uuid.uuid4())  # Gera um nome aleatório
        new_filename = f"{random_name}.{ext}"  # Cria o novo nome do arquivo
        return new_filename
    return filename  # Retorna o nome original se for None


class InscricaoView(LoginRequiredMixin, CreateView):
    model = Inscricao
    fields = ('nomeacao', 'diploma', 'diploma1', 'diploma2', 'opcao1', 'opcao2', 'opcao3')
    template_name = 'inscricao/inscricao.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('inscricao:concurso')

    def form_valid(self, form):
        info = form.save(commit=False)
        professor = Professor.objects.get(id=self.request.user.id)
        info.professor = professor
        info.nomeacao.name = generate_random_filename(info.nomeacao.name)
        info.diploma.name = generate_random_filename(info.diploma.name)
        info.diploma1.name = generate_random_filename(info.diploma1.name)
        info.diploma2.name = generate_random_filename(info.diploma2.name)
        info.save()
        return super().form_valid(form)


class InfoAcademicas(LoginRequiredMixin, CreateView):
    model = InformacoesAcademicas
    fields = ('area_formacao', 'especializacao', 'area_especializacao', 'anexo')
    template_name = 'inscricao/info_academicas.html'
    context_object_name = 'form'


    def get_success_url(self):
        return reverse_lazy('inscricao:certificado')

    def form_valid(self, form):
        info = form.save(commit=False)
        info.status = True
        info.anexo.name = generate_random_filename(info.anexo.name)
        info.save()
        professor = Professor.objects.get(id=self.request.user.id)
        inscricao = Inscricao.objects.get(professor=professor)
        inscricao.informacoes_academicas = info
        inscricao.save()
        return super().form_valid(form)


class Concurso1(LoginRequiredMixin, CreateView):
    model = Concurso
    fields = ('realizacao', 'area', 'posse')
    template_name = 'inscricao/concurso.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('inscricao:academica')

    def form_valid(self, form):
        concurso = form.save(commit=False)
        concurso.status = True
        concurso.save()
        professor = Professor.objects.get(id=self.request.user.id)
        inscricao = Inscricao.objects.get(professor=professor)
        inscricao.concurso = concurso
        inscricao.save()
        return super().form_valid(form)

@login_required
def certificadoTeste(request):
    CertificaFormSet = modelformset_factory(Certificado, form=CertificadoForm, extra=6, max_num=6)
    if request.method == 'POST':
        formset = CertificaFormSet(request.POST, request.FILES, queryset=Certificado.objects.none())
        if formset.is_valid():
            professor = Professor.objects.get(id=request.user.id)
            inscricao = Inscricao.objects.get(professor=professor)
            for form in formset:
                questao = form.save(commit=False)
                questao.inscricao = inscricao
                questao.certificado.name = generate_random_filename(questao.certificado.name)
                questao.save()

            url = reverse_lazy('inscricao:requerimento')
            return HttpResponseRedirect(url)
    else:
        formset = CertificaFormSet(queryset=Certificado.objects.none())
    return render(request, 'inscricao/certificado.html', {'formset': formset})

@login_required
def requerimentoTeste(request):
    RequerimentoFormSet = formset_factory(RequerimentoForm, extra=6, max_num=6)
    professor = Professor.objects.get(id=request.user.id)
    inscricao = Inscricao.objects.get(professor=professor)
    if request.method == 'POST':
        formset = RequerimentoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            contador = 0
            ano = 2021
            for form in formset:
                if form.is_valid():
                    questao = form.save(commit=False)
                    questao.inscricao = inscricao
                    if contador != 0 and contador % 2 == 0:
                        ano += 1
                        questao.semestre = f'{contador + 1}º Semestre - {ano}'
                    else:
                        questao.semestre = f'{contador + 1}º Semestre - {ano}'
                    questao.anexo.name = generate_random_filename(questao.anexo.name)
                    questao.save()
                    contador += 1
                    print(contador)


            # Redirecionar após salvar os formulários
            url = reverse_lazy('inscricao:termo', kwargs={'pk': inscricao.pk})
            return HttpResponseRedirect(url)
    else:
        formset = RequerimentoFormSet()

    return render(request, 'inscricao/requerimento.html', {'formset': formset})


class Termo(LoginRequiredMixin, UpdateView):
    model = Inscricao
    fields = ('termo',)
    template_name = 'inscricao/termo.html'

    def get_success_url(self):
        return reverse('professor:detalhes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inscricao = Inscricao.objects.get(pk=self.kwargs['pk'])
        professor = Professor.objects.get(id=inscricao.professor.id)
        context['professor'] = professor
        return context


## classes auxiliares

class InfoAcademicasUp(LoginRequiredMixin, CreateView):
    model = InformacoesAcademicas
    fields = ('area_formacao', 'especializacao', 'area_especializacao', 'anexo')
    template_name = 'inscricao/up_info_academicas.html'
    context_object_name = 'form'


    def get_success_url(self):
        return reverse_lazy('professor:detalhes')

    def form_valid(self, form):
        info = form.save(commit=False)
        info.status = True
        info.anexo.name = generate_random_filename(info.anexo.name)
        info.save()
        professor = Professor.objects.get(id=self.request.user.id)
        inscricao = Inscricao.objects.get(professor=professor)
        inscricao.informacoes_academicas = info
        inscricao.save()
        return super().form_valid(form)


class ConcursoDetail(LoginRequiredMixin, CreateView):
    form_class = ConcursoForm
    template_name = 'inscricao/up_concurso.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('professor:detalhes')

    def form_valid(self, form):
        concurso = form.save(commit=False)
        concurso.status = True
        concurso.save()
        professor = Professor.objects.get(id=self.request.user.id)
        inscricao = Inscricao.objects.get(professor=professor)
        inscricao.concurso = concurso
        inscricao.save()
        return super().form_valid(form)


@login_required
def certificadoUp(request):
    CertificaFormSet = modelformset_factory(Certificado, form=CertificadoForm, extra=6, max_num=6)
    if request.method == 'POST':
        formset = CertificaFormSet(request.POST, request.FILES, queryset=Certificado.objects.none())
        if formset.is_valid():
            professor = Professor.objects.get(id=request.user.id)
            inscricao = Inscricao.objects.get(professor=professor)
            for form in formset:
                questao = form.save(commit=False)
                questao.inscricao = inscricao
                questao.certificado.name = generate_random_filename(questao.certificado.name)
                questao.save()

            url = reverse_lazy('professor:detalhes')
            return HttpResponseRedirect(url)
    else:
        formset = CertificaFormSet(queryset=Certificado.objects.none())
    return render(request, 'inscricao/up_certificado.html', {'formset': formset})


@login_required
def requerimentoUp(request):
    RequerimentoFormSet = modelformset_factory(RequerimentoAmpliacao, form=RequerimentoForm, extra=6, max_num=6)
    professor = Professor.objects.get(id=request.user.id)
    inscricao = Inscricao.objects.get(professor=professor)
    formset = RequerimentoFormSet()
    if request.method == 'POST':
        formset = RequerimentoFormSet(request.POST, request.FILES, queryset=RequerimentoAmpliacao.objects.none())
        contador = 0
        ano = 2021
        if formset.is_valid():
            for form in formset:
                questao = form.save(commit=False)
                questao.inscricao = inscricao
                if contador != 0 and contador % 2 == 0:
                    ano += 1
                    questao.semestre = f'{contador + 1}º Semestre - {ano}'
                else:
                    questao.semestre = f'{contador + 1}º Semestre - {ano}'

                questao.anexo.name = generate_random_filename(questao.anexo.name)
                questao.save()
                contador+=1
            formset.save()

            url = reverse_lazy('professor:detalhes')
            return HttpResponseRedirect(url)
    else:
        formset = RequerimentoFormSet(queryset=RequerimentoAmpliacao.objects.none())
    return render(request, 'inscricao/up_requerimento.html',
                  {'formset': formset})


class TermoUP(LoginRequiredMixin, UpdateView):
    model = Inscricao
    fields = ('termo',)
    template_name = 'inscricao/up_termo.html'

    def get_success_url(self):
        return reverse('professor:detalhes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inscricao = Inscricao.objects.get(pk=self.kwargs['pk'])
        professor = Professor.objects.get(id=inscricao.professor.id)
        context['professor'] = professor
        return context


## classes de analise

def analisarIncricao(request, pk):
    professor = Professor.objects.get(pk=pk)
    inscricao = Inscricao.objects.get(professor=professor)
    certificados = Certificado.objects.filter(inscricao=inscricao)
    ampliacoes = RequerimentoAmpliacao.objects.filter(inscricao=inscricao)
    results = None

    try:
        results = Resultado.objects.get(inscricao=inscricao)
    except:
        print('')

    cursos = []
    ampliacoes_list = []
    for certificado in certificados:
        if certificado.curso != '':
            cursos.append(certificado)

    for amp in ampliacoes:
        if amp.escola != None:
            ampliacoes_list.append(amp)

    if request.method == 'POST':
        form = ResultadoForm(request.POST)
        print(form)
        if form.is_valid():
            resultado, created = Resultado.objects.get_or_create(inscricao=inscricao)
            resultado.resultado = form.cleaned_data['resultado']
            resultado.comentario = form.cleaned_data['comentario']
            resultado.save()

            inscricao.analisado = True
            inscricao.save()

            url = reverse_lazy('professor:administrador')
            return HttpResponseRedirect(url)
    else:
        form = ResultadoForm(instance=results)

    contexto = {'form': form, 'professor': professor, 'certificados': cursos, 'ampliacoes': ampliacoes_list}
    return render(request, 'inscricao/resultado.html', contexto)


def resumo(request, pk):
    professor = Professor.objects.get(pk=pk)
    inscricao = Inscricao.objects.get(professor=professor)
    certificados = Certificado.objects.filter(inscricao=inscricao)
    ampliacoes = RequerimentoAmpliacao.objects.filter(inscricao=inscricao)
    results = None
    complementos = False

    try:
        results = Resultado.objects.get(inscricao=inscricao)
    except:
        print('')

    try:
        complementos = AmpliacaoComplemento.objects.filter(inscricao=inscricao)
    except:
        print('')

    cursos = []
    ampliacoes_list = []
    complementos_list = []
    for certificado in certificados:
        if certificado.curso != '':
            cursos.append(certificado)

    for amp in ampliacoes:
        if amp.escola != None:
            ampliacoes_list.append(amp)

    for complemento in complementos:
        if complemento.escola != None:
            complementos_list.append(complemento)

    pos_pontos = None
    try:
        pos_pontos = PosTotalPontos.objects.get(inscricao=inscricao)
    except:
        print('')

    pontos = None
    try:
        pontos = TotalPontos.objects.get(inscricao=inscricao)
    except:
        print('')

    experiencia = None
    try:
        experiencia = Experiencia.objects.get(inscricao=inscricao)
    except:
        print('')

    contexto = {'professor': professor, 'certificados': cursos, 'ampliacoes': ampliacoes_list,
                'resultado': results, 'complementos': complementos_list, 'pontos': pontos,
                'experiencia': experiencia, 'pos': pos_pontos}
    return render(request, 'inscricao/resumo.html', contexto)


def update_status(request, pk):
    professor = get_object_or_404(Professor, pk=pk)
    inscricao = get_object_or_404(Inscricao, professor=professor)

    resultado = None
    try:
        resultado = Resultado.objects.get(inscricao=inscricao)

    except:
        print('Resultado Error')

    pontos = None
    total_p = 0
    try:
        pontos = TotalPontos.objects.get(inscricao=inscricao)
        total_p = pontos.total_pontos
    except:
        print('')

    total_pos = None
    try:
        total_pos = PosTotalPontos.objects.get(inscricao=inscricao)
    except:
        print('')

    experiencia = None
    try:
        experiencia = Experiencia.objects.get(inscricao=inscricao)
    except:
        print('')

    informacoes_acad = get_object_or_404(InformacoesAcademicas, id=inscricao.informacoes_academicas.id)
    certificados = get_list_or_404(Certificado, inscricao=inscricao)
    ampliacoes = get_list_or_404(RequerimentoAmpliacao, inscricao=inscricao)
    complemento = False

    try:
        complemento = AmpliacaoComplemento.objects.filter(inscricao=inscricao)
    except:
        print('Complemento ERROR')

    cursos = []
    for certificado in certificados:
        if certificado.curso != '':
            cursos.append(certificado)

    CertificadoFormSet = inlineformset_factory(Inscricao, Certificado, form=CertificadoForm, extra=0, can_delete=False)
    RequerimentoFormSet = inlineformset_factory(Inscricao, RequerimentoAmpliacao, form=RequerimentoAmpliacaoCheck, extra=0, can_delete=False)
    ComplementoFormSet = False

    if complemento != False:
        ComplementoFormSet = inlineformset_factory(Inscricao, AmpliacaoComplemento, form=ComplementoCheck, extra=0, can_delete=False)
        print(f'FormSet: {ComplementoFormSet}')

    if request.method == 'POST':
        # Atualiza o status de cada instância com base nos dados do formulário
        certificado_formset = CertificadoFormSet(request.POST, instance=inscricao, prefix='certificado')
        inscricao_form = InscricaoCheck(request.POST, instance=inscricao)
        informacoes_form = InformacoesCheck(request.POST, instance=informacoes_acad)
        pontos_form = PontosForm(request.POST, instance=pontos)
        pos_form = PosPontosForm(request.POST, instance=total_pos)
        experiencia_form = ExperienciaForm(request.POST, instance=experiencia)
        requerimento_formset = RequerimentoFormSet(request.POST, instance=inscricao, prefix='requerimento')

        if complemento != False:
            complemento_formset = ComplementoFormSet(request.POST, instance=inscricao)

            if (informacoes_form.is_valid() and inscricao_form.is_valid() and
                    certificado_formset.is_valid() and requerimento_formset.is_valid() and complemento_formset.is_valid()
                    and pontos_form.is_valid() and experiencia_form.is_valid() and pos_form.is_valid()):

                certificado_formset.save()
                requerimento_formset.save()
                complemento_formset.save()
                pf = pontos_form.save(commit=False)
                pf.inscricao = inscricao
                pf.save()
                pfs = pos_form.save(commit=False)
                pfs.inscricao = inscricao
                pfs.save()
                pf1 = experiencia_form.save(commit=False)
                pf1.inscricao = inscricao
                pf1.save()
                ifo = inscricao_form.save(commit=False)
                ifo1 = inscricao_form.cleaned_data['visto']
                ifo.check = ifo1
                ifo.save()
                info = informacoes_form.save(commit=False)

                if informacoes_form.cleaned_data['info_visto']:
                    info1 = informacoes_form.cleaned_data['info_visto']
                    info.info_visto = info1
                    info.save()

                url = reverse_lazy('inscricao:up_teste', kwargs={'pk': professor.pk})
                return HttpResponseRedirect(url)
        else:
            if (informacoes_form.is_valid() and inscricao_form.is_valid() and
                    certificado_formset.is_valid() and requerimento_formset.is_valid() and
                    pontos_form.is_valid() and experiencia_form.is_valid() and pos_form.is_valid()):

                certificado_formset.save()
                pf = pontos_form.save(commit=False)
                pf.inscricao = inscricao
                pf.save()
                pfs = pos_form.save(commit=False)
                pfs.inscricao = inscricao
                pfs.save()
                pf1 = experiencia_form.save(commit=False)
                pf1.inscricao = inscricao
                pf1.save()
                requerimento_formset.save()
                ifo = inscricao_form.save(commit=False)
                ifo1 = inscricao_form.cleaned_data['visto']
                ifo.check = ifo1
                ifo.save()
                info = informacoes_form.save(commit=False)

                if informacoes_form.cleaned_data['info_visto']:
                    info1 = informacoes_form.cleaned_data['info_visto']
                    info.info_visto = info1
                    info.save()

                url = reverse_lazy('inscricao:up_teste', kwargs={'pk': professor.pk})
                return HttpResponseRedirect(url)

    else:
        # Se não for uma solicitação POST, exibe os formulários preenchidos com os dados existentes
        certificado_formset = CertificadoFormSet(instance=inscricao, prefix='certificado')
        requerimento_formset = RequerimentoFormSet(instance=inscricao, prefix='requerimento')
        inscricao_form = InscricaoCheck(instance=inscricao)
        informacoes_form = InformacoesCheck(instance=informacoes_acad)
        pontos_form = PontosForm(instance=pontos)
        pos_form = PosPontosForm(instance=total_pos)
        experiencia_form = ExperienciaForm(instance=experiencia)
        complemento_formset = None

        if complemento != False:
            complemento_formset = ComplementoFormSet(instance=inscricao)


    # Renderiza a página com os formulários
    return render(request, 'inscricao/analise.html', {
        'certificado_formset': certificado_formset,
        'inscricao_form': inscricao_form,
        'informacoes_form': informacoes_form,
        'complemento_formset': complemento_formset,
        'requerimento_formset': requerimento_formset,
        'professor': professor,
        'ampliacoes': ampliacoes,
        'certificados': certificados,
        'resultado': resultado,
        'complemento': complemento,
        'pontos': pontos_form,
        'pos_form': pos_form,
        'experiencia': experiencia_form,
        'total': total_p,
        'total_pos': total_pos,
        'experiencia1': experiencia,
    })


###### RELATÓRIOS ######


class RelatorioPDF(View):
    def get(self, request, *args, **kwargs):
        # Recupera o objeto Inscricao
        professor = get_object_or_404(Professor, pk=self.kwargs['pk'])
        inscricao = Inscricao.objects.get(professor=professor)

        # Cria o objeto response com o cabeçalho do PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="relatorio.pdf"'

        # Criação do objeto PDF usando o ReportLab
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Criação de uma lista para conter todos os elementos do PDF
        elements = []

        # Adiciona o título ao PDF
        title_style = ParagraphStyle(name='TitleStyle', fontSize=16, spaceAfter=12)
        title = Paragraph("Relatório da Inscrição", title_style)
        elements.append(title)

        # Adiciona informações de cada inscrição ao PDF
        data = [
            ["Professor", inscricao.professor.nome],
            ["Inscrição", inscricao.concurso.area],
        ]

        # Cria a tabela
        table = Table(data, colWidths=150, rowHeights=30)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        # Aplica o estilo à tabela
        table.setStyle(style)

        # Adiciona a tabela à lista de elementos
        elements.append(table)

        # Constrói o PDF
        doc.build(elements)

        # Move o ponteiro para o início do buffer antes de enviar a resposta
        buffer.seek(0)
        response.write(buffer.read())

        return response


@login_required
def requerimentoComplemento(request):
    professor = Professor.objects.get(id=request.user.id)
    inscricao = Inscricao.objects.get(professor=professor)
    adendo = False
    try:
        anteriores = AmpliacaoComplemento.objects.filter(inscricao=inscricao)
        if len(anteriores) > 0:
            adendo = True
    except:
        adendo = False

    RequerimentoFormSet = formset_factory(ComplementoForm, extra=6, max_num=6)
    complemento = None
    try:
        complemento = AmpliacaoComplemento.objects.filter(inscricao=inscricao)
    except:
        print('ERROR')

    if request.method == 'POST':
        formset = RequerimentoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    questao = form.save(commit=False)
                    questao.inscricao = inscricao
                    questao.anexo.name = generate_random_filename(questao.anexo.name)
                    questao.save()

            url = reverse_lazy('professor:detalhes')
            return HttpResponseRedirect(url)
    else:
        formset = RequerimentoFormSet()

    return render(request, 'inscricao/requerimentoComplemento.html', {'formset': formset, 'adendo': adendo})


class RecursoView(LoginRequiredMixin, CreateView):
    form_class = RecursoForm
    template_name = 'inscricao/recurso.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('professor:detalhes')

    def form_valid(self, form):
        info = form.save(commit=False)
        professor = Professor.objects.get(id=self.request.user.id)
        inscricao = Inscricao.objects.get(professor=professor)
        info.inscricao = inscricao
        info.documento.name = generate_random_filename(info.documento.name)
        info.documento_1.name = generate_random_filename(info.documento_1.name)
        info.documento_2.name = generate_random_filename(info.documento_2.name)
        info.save()
        return super().form_valid(form)


def analisarRecurso(request, pk):
    professor = Professor.objects.get(pk=pk)
    inscricao = Inscricao.objects.get(professor=professor)
    recurso_recurso = None
    results_recurso = None

    try:
        recurso_recurso = Recurso.objects.get(inscricao=inscricao)
    except:
        print('Print')

    try:
        results_recurso = ResultadoRecurso.objects.get(recurso=recurso_recurso)
    except:
        print('')

    if request.method == 'POST':
        form = ResultadoRecursoForm(request.POST)
        if form.is_valid():
            resultado_recurso, created = ResultadoRecurso.objects.get_or_create(recurso=recurso_recurso)
            resultado_recurso.resultado = form.cleaned_data['resultado']

            resultado_recurso.comentario = form.cleaned_data['comentario']
            resultado_recurso.recurso_visto = True
            resultado_recurso.recurso = recurso_recurso
            resultado_recurso.save()

            inscricao.analisado = True
            inscricao.save()

            url = reverse_lazy('professor:administrador')
            return HttpResponseRedirect(url)
    else:
        form = ResultadoRecursoForm(instance=results_recurso)

    contexto = {'form': form, 'professor': professor, 'recurso': recurso_recurso}
    return render(request, 'inscricao/resultado_recurso.html', contexto)
