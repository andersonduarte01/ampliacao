from django.db import models
from ..core.models import Usuario
from cpf_field.models import CPFField
from stdimage import StdImageField
# Create your models here.


class Professor(Usuario):
    foto = StdImageField(upload_to='Imagens/perfil',
                         variations={'thumbnail': {'width': 600, 'height': 800}})
    lotado = models.CharField(verbose_name='Escola', max_length=120, help_text='Escola em que esta lotado')
    data_nascimento = models.CharField(verbose_name='Data de Nascimento', null=True, blank=True, help_text='dd/mm/aaaa', max_length=12)
    rg = models.CharField(verbose_name='RG', max_length=20)
    matricula = models.CharField(verbose_name='Matrícula', max_length=50)
    cpf = CPFField('CPF')
    telefone = models.CharField(verbose_name='Telefone', max_length=20, null=True, blank=True)
    rua = models.CharField(verbose_name='Rua', max_length=100)
    numero = models.CharField(verbose_name='Número', max_length=20)
    complemento = models.CharField(verbose_name='Complemento', max_length=200, blank=True, null=True)
    bairro = models.CharField(verbose_name='Bairro', max_length=100)

    def __str__(self):
        return self.nome

    def imagem(self):
        if self.foto:
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
