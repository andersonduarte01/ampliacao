from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def is_administatot(user):
    return user.is_authenticated and user.is_administrator


class StaffRequiredMixin(UserPassesTestMixin):
    login_url = reverse_lazy('professor:detalhes')  # Redireciona para a página de login caso o acesso seja negado

    def test_func(self):
        return is_administatot(self.request.user)




