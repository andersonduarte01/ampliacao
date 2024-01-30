from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from ..inscricao.concluir import analisarInscricao
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, ListView

from .models import Professor
from ..inscricao.models import Inscricao, Documento, Certificado, RequerimentoAmpliacao, AmpliacaoComplemento, Resultado
from .forms import UserCreationProfessor
from ..inscricao.decoradores import StaffRequiredMixin

# Create your views here.


class CadastrarProfessor(SuccessMessageMixin, CreateView):
    model = Professor
    form_class = UserCreationProfessor
    template_name = 'professor/adicionar_professor.html'
    success_message = 'Cadastro Realizado com sucesso!'
    success_url = reverse_lazy('professor:detalhes')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, email=username, password=password)
        if user:
            login(self.request, user)
        return response


class DetalhesInscricao(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'professor/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inscricao = ''
        info_acad = ''
        concurso = ''
        certificados = ''
        carga_horaria = ''
        termo = False
        adendo = False
        documento = ''

        try:
            documento = Documento.objects.filter(id=1)
        except:
            print('')

        professor = Professor.objects.get(id=self.request.user.id)
        try:
            inscricao = Inscricao.objects.get(professor=professor)
            termo = inscricao.termo
        except:
            inscricao = False

        try:
            info_acad = inscricao.informacoes_academicas
        except:
            info_acad = False

        try:
            concurso = inscricao.concurso
        except:
            concurso = False

        try:
            certificados = Certificado.objects.filter(inscricao=inscricao)
        except:
            certificados = False

        try:
            carga_horaria = RequerimentoAmpliacao.objects.filter(inscricao=inscricao)
        except:
            carga_horaria = False

        try:
            anteriores = AmpliacaoComplemento.objects.filter(inscricao=inscricao)
            if len(anteriores) > 0:
                adendo = True
        except:
            adendo = False

        if inscricao:
            analisarInscricao(inscricao=inscricao, info_acad=info_acad, concurso=concurso,
                              certificados=certificados, carga_horaria=carga_horaria, termo=termo)

        context['professor'] = professor
        context['inscricao'] = inscricao
        context['info_acad'] = info_acad
        context['concurso'] = concurso
        context['certificados'] = certificados
        context['carga'] = carga_horaria
        context['termo'] = termo
        context['documento'] = documento
        print(adendo)
        context['adendo'] = adendo
        return context


class ResultadoAmp(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'professor/resultado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        professor = Professor.objects.get(id=self.request.user.id)
        inscricao = Inscricao.objects.get(professor=professor)
        resultado = Resultado.objects.get(inscricao=inscricao)
        context['professor'] = professor
        context['resultado'] = resultado
        return context


class AtualizarProfessor(SuccessMessageMixin, UpdateView):
    model = Professor
    fields = ('foto', 'nome', 'data_nascimento', 'matricula', 'rg', 'cpf', 'telefone',
              'rua', 'numero', 'complemento', 'bairro')
    template_name = 'professor/atualizar_professor.html'
    success_message = 'Cadastro Atualizado com sucesso!'
    success_url = reverse_lazy('professor:detalhes')


class PainelAdm(StaffRequiredMixin, TemplateView):
    template_name = 'professor/painel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concluidos'] = Inscricao.inscricoes_concluidas().count()
        context['analisadas'] = Inscricao.inscricoes_analisadas().count()
        context['pendentes'] = Inscricao.inscricoes_pendentes().count()
        return context


## Tabelas

class ProfessoresList(StaffRequiredMixin, ListView):
    model = Professor
    template_name = 'professor/lista.html'
    context_object_name = 'professores'

    def get_queryset(self):
        return Professor.objects.filter(is_administrator=False)


class InscricoesList(StaffRequiredMixin, ListView):
    model = Inscricao
    template_name = 'professor/lista_inscricoes_negadas.html'
    context_object_name = 'inscricoes'

    def get_queryset(self):
        insc = Inscricao.inscricoes_analisadas()
        inscricoes = []
        for inscricao in insc:
            if inscricao.resultado.resultado == 'Negado':
                inscricoes.append(inscricao)
        return inscricoes


class InscricoesPendentes(StaffRequiredMixin, ListView):
    model = Inscricao
    template_name = 'professor/inscricoes_pendentes.html'
    context_object_name = 'inscricoes_pendentes'

    def get_queryset(self):
        return Inscricao.inscricoes_pendentes()


class InscricoesAnalisadas(StaffRequiredMixin, ListView):
    model = Inscricao
    template_name = 'professor/inscricoes_analisadas_aprovadas.html'
    context_object_name = 'inscricoes_analisadas'

    def get_queryset(self):
        insc = Inscricao.inscricoes_analisadas()
        inscricoes = []
        for inscricao in insc:
            if inscricao.resultado.resultado == 'Aprovado':
                inscricoes.append(inscricao)
        return inscricoes


class InscricoesOutros(StaffRequiredMixin, ListView):
    model = Inscricao
    template_name = 'professor/inscricoes_outros.html'
    context_object_name = 'inscricoes_analisadas'

    def get_queryset(self):
        insc = Inscricao.inscricoes_analisadas()
        inscricoes = []
        for inscricao in insc:
            if inscricao.resultado.resultado == 'Selecione':
                inscricoes.append(inscricao)
        return inscricoes


class InscricoesComplementos(StaffRequiredMixin, ListView):
    model = Inscricao
    template_name = 'professor/inscricoes_complementos.html'
    context_object_name = 'inscricoes_complementos'

    def get_queryset(self):
        insc = Inscricao.objects.all()
        inscricoes = []
        for inscricao in insc:
            if AmpliacaoComplemento.objects.filter(inscricao=inscricao):
                inscricoes.append(inscricao)
        return inscricoes


class InscricoesIncompletas(StaffRequiredMixin, ListView):
    model = Inscricao
    template_name = 'professor/inscricoes_incompletas.html'
    context_object_name = 'inscricoes_incompletas'

    def get_queryset(self):
        return Inscricao.inscricoes_incompletas()
