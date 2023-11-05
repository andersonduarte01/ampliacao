from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView

from .forms import CertificadoForm, RequerimentoForm, ConcursoForm
from .models import Inscricao, InformacoesAcademicas, Concurso, RequerimentoAmpliacao, Certificado, Resultado
from ..professor.models import Professor
from ..inscricao.decoradores import StaffRequiredMixin

class InscricaoView(LoginRequiredMixin, CreateView):
    model = Inscricao
    fields = ('nomeacao', 'diploma', 'opcao1', 'opcao2', 'opcao3')
    template_name = 'inscricao/inscricao.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('inscricao:concurso')

    def form_valid(self, form):
        info = form.save(commit=False)
        professor = Professor.objects.get(id=self.request.user.id)
        info.professor = professor
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
        info.save()
        professor = Professor.objects.get(id=self.request.user.id)
        inscricao = Inscricao.objects.get(professor=professor)
        inscricao.informacoes_academicas = info
        inscricao.save()
        return super().form_valid(form)


class Concurso(LoginRequiredMixin, CreateView):
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
                questao.save()

            url = reverse_lazy('inscricao:requerimento')
            return HttpResponseRedirect(url)
    else:
        formset = CertificaFormSet(queryset=Certificado.objects.none())
    return render(request, 'inscricao/certificado.html', {'formset': formset})

@login_required
def requerimentoTeste(request):

    RequerimentoFormSet = modelformset_factory(RequerimentoAmpliacao, form=RequerimentoForm, extra=6, max_num=6)
    professor = Professor.objects.get(id=request.user.id)
    inscricao = Inscricao.objects.get(professor=professor)
    formset = RequerimentoFormSet()
    if request.method == 'POST':
        formset = RequerimentoFormSet(request.POST, request.FILES, queryset=RequerimentoAmpliacao.objects.none())
        if formset.is_valid():
            for form in formset:
                questao = form.save(commit=False)
                questao.inscricao = inscricao
                questao.save()
            formset.save()

            url = reverse_lazy('inscricao:termo', kwargs={'pk': inscricao.pk})
            return HttpResponseRedirect(url)
    else:
        formset = RequerimentoFormSet(queryset=RequerimentoAmpliacao.objects.none())
    return render(request, 'inscricao/requerimento.html',
                  {'formset': formset})


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
        if formset.is_valid():
            for form in formset:
                questao = form.save(commit=False)
                questao.inscricao = inscricao
                questao.save()
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

class AnalisarIncricao(StaffRequiredMixin, CreateView):
    model = Resultado
    template_name = 'inscricao/resultado.html'
    fields = ('resultado', 'comentario')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        professor = Professor.objects.get(pk=self.kwargs['pk'])
        contexto['professor'] = professor
        return contexto