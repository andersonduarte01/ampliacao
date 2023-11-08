from django import forms
from django.forms import FileInput, TextInput, Select

from .models import Inscricao, Certificado, RequerimentoAmpliacao, Concurso


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


