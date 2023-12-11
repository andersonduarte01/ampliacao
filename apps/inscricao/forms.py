from django import forms
from django.forms import FileInput, TextInput, Select

from .models import Inscricao, Certificado, RequerimentoAmpliacao, Concurso, InformacoesAcademicas


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


class ConcursoCheck(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = ['visto', ]
        labels = {
            'visto': '',  # Define a label como uma string vazia para remover o rótulo
        }


class RequerimentoAmpliacaoCheck(forms.ModelForm):
    class Meta:
        model = RequerimentoAmpliacao
        fields = ['requerimento_visto', ]
        labels = {
            'requerimento_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }


class InscricaoCheck(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['visto', ]
        labels = {
            'visto': '',  # Define a label como uma string vazia para remover o rótulo
        }


class InformacoesCheck(forms.ModelForm):
    class Meta:
        model = InformacoesAcademicas
        fields = ['info_visto', ]
        labels = {
            'info_visto': '',  # Define a label como uma string vazia para remover o rótulo
        }
