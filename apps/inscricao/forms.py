from django import forms
from django.forms import FileInput, TextInput, Select, Textarea

from .models import Inscricao, Certificado, RequerimentoAmpliacao, Concurso, InformacoesAcademicas, Resultado, AmpliacaoComplemento


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

    #opcao = forms.ChoiceField(widget=forms.RadioSelect, choices=RequerimentoAmpliacao.RESPOSTA)


class ConcursoForm(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = ['realizacao', 'area', 'posse']


class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['certificado_visto', ]
        labels = {
            'certificado_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
        widgets = {
            'certificado_visto': Select(
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
