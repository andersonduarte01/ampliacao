from django import forms
from django.core.exceptions import ValidationError
from ..professor.models import Professor


class UserCreationProfessor(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = ('foto', 'nome', 'lotado', 'data_nascimento', 'matricula', 'rg', 'cpf', 'telefone', 'rua', 'numero', 'complemento', 'bairro', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user