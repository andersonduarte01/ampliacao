from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def is_administatot(user):
    return user.is_authenticated and user.is_administrator


class StaffRequiredMixin(UserPassesTestMixin):
    login_url = reverse_lazy('professor:detalhes')  # Redireciona para a página de login caso o acesso seja negado

    def test_func(self):
        return is_administatot(self.request.user)


def validate_pdf_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Permitido apenas arquivos em formato PDF.')
