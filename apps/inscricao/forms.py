from django import forms
from django.forms import FileInput, TextInput, Select, Textarea, NumberInput

from .models import Inscricao, Certificado, RequerimentoAmpliacao, Concurso, InformacoesAcademicas, Resultado, \
    AmpliacaoComplemento, TotalPontos, Experiencia, PosTotalPontos, Recurso, ResultadoRecurso


class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['curso', 'certificado']
        widgets = {
            'certificado': FileInput(
                attrs={'class': 'form-control'}),
            'curso': TextInput(
                attrs={'class': 'form-control'}),
        }


class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['professor', 'nomeacao', 'diploma']


class RequerimentoForm(forms.ModelForm):
    class Meta:
        model = RequerimentoAmpliacao
        fields = ['escola', 'opcao', 'cargo', 'anexo']
        widgets = {
            'opcao': Select(
                attrs={'class': 'form-control'}),
            'escola': TextInput(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'anexo': FileInput(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; margin-top: 15px;'}),
            'cargo': TextInput(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; margin-top: 15px;'}),
        }

    # opcao = forms.ChoiceField(widget=forms.RadioSelect, choices=RequerimentoAmpliacao.RESPOSTA)


class ConcursoForm(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = ['realizacao', 'area', 'posse']


class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['certificado_visto', 'pontuacao']
        labels = {
            'certificado_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
        widgets = {
            'certificado_visto': Select(
                attrs={'class': 'form-control'}),
            'pontuacao': Select(
                attrs={'class': 'form-control'}),
        }


class ConcursoCheck(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = ['concurso_visto', ]
        labels = {
            'concurso_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
        widgets = {
            'concurso_visto': Select(
                attrs={'class': 'form-control'}),
        }


class RequerimentoAmpliacaoCheck(forms.ModelForm):
    class Meta:
        model = RequerimentoAmpliacao
        fields = ['requerimento_visto', ]
        labels = {
            'requerimento_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
        widgets = {
            'requerimento_visto': Select(
                attrs={'class': 'form-control'}),
        }


class InscricaoCheck(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['visto', ]
        labels = {
            'visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
        widgets = {
            'visto': Select(
                attrs={'class': 'form-control'}),
        }
        widgets = {
            'visto': Select(
                attrs={'class': 'form-control'}),
        }


class InformacoesCheck(forms.ModelForm):
    class Meta:
        model = InformacoesAcademicas
        fields = ['info_visto', ]
        labels = {
            'info_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
        widgets = {
            'info_visto': Select(
                attrs={'class': 'form-control'}),
        }


class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['resultado', 'comentario']
        widgets = {
            'resultado': Select(
                attrs={'class': 'form-control'}),
            'comentario': Textarea(
                attrs={'class': 'form-control'}),
        }


class ResultadoRecursoForm(forms.ModelForm):
    class Meta:
        model = ResultadoRecurso
        fields = ['resultado', 'comentario']
        widgets = {
            'resultado': Select(
                attrs={'class': 'form-control'}),
            'comentario': Textarea(
                attrs={'class': 'form-control'}),
        }


class ComplementoForm(forms.ModelForm):
    class Meta:
        model = AmpliacaoComplemento
        fields = ['semestre', 'escola', 'opcao', 'cargo', 'anexo']
        widgets = {
            'semestre': TextInput(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;', 'placeholder': 'Semestre - Ano'}),
            'opcao': Select(
                attrs={'class': 'form-control'}),
            'escola': TextInput(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'anexo': FileInput(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; margin-top: 15px;'}),
            'cargo': TextInput(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 10px; margin-top: 15px;'}),
        }


class ComplementoCheck(forms.ModelForm):
    class Meta:
        model = AmpliacaoComplemento
        fields = ['complemento_visto', ]
        labels = {
            'complemento_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
        widgets = {
            'complemento_visto': Select(
                attrs={'class': 'form-control'}),
        }


class PontosForm(forms.ModelForm):
    class Meta:
        model = TotalPontos
        fields = ['total_pontos', ]
        widgets = {
            'total_pontos': Select(
                attrs={'class': 'form-control'}),
        }


class PosPontosForm(forms.ModelForm):
    class Meta:
        model = PosTotalPontos
        fields = ['pos_pontos', ]
        widgets = {
            'pos_pontos': Select(
                attrs={'class': 'form-control'}),
        }


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['anos_experiencia', 'pontos_experiencia']
        widgets = {
            'anos_experiencia': TextInput(
                attrs={'class': 'form-control'}),
            'pontos_experiencia': Select(
                attrs={'class': 'form-control'}),
        }


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ['razoes', 'documento', 'documento_1', 'documento_2']
        widgets = {
            'documento': FileInput(attrs={'class': 'form-control'}),
            'documento_1': FileInput(attrs={'class': 'form-control'}),
            'documento_2': FileInput(attrs={'class': 'form-control'}),
            'razoes': Textarea(attrs={'class': 'form-control'}),
        }
