from django.db import models
from ..professor.models import Professor
from .decoradores import validate_pdf_extension


class InformacoesAcademicas(models.Model):
    RESPOSTA = [
        ('SIM', 'SIM'),
        ('NÃO', 'NÃO'),
    ]
    area_formacao = models.CharField(verbose_name='Formação', max_length=180,
                                     help_text='Caso tenha marcado sim em graduação', null=True, blank=True)
    especializacao = models.CharField(verbose_name='Curso de Especialização (Pós Graduação Lato sensu)',
                                      choices=RESPOSTA, default='NÃO', max_length=20)
    area_especializacao = models.CharField(verbose_name='Especialização e/ou Habilitação', max_length=180,
                                     help_text='Caso tenha marcado sim em especialização', null=True,
                                           blank=True)
    anexo = models.FileField(upload_to='docs/nomeacao', verbose_name='Anexar arquivo', null=True, blank=True,
                             help_text='Anexar arquivo referente a Especialização e/ou Habilitação',
                             max_length=300, validators=[validate_pdf_extension])
    status = models.BooleanField(verbose_name='Concluido', default=False)
    info_visto = models.BooleanField(verbose_name='Check', default=False)

    def anexoChecar(self):
        if self.anexo:
            return True
        else:
            return False

class Concurso(models.Model):
    realizacao = models.CharField(verbose_name='Ano de realização do Concurso', max_length=12)
    area = models.CharField(verbose_name='Cargo do Concurso', max_length=80)
    posse = models.CharField(verbose_name='Data da posse do Concurso', max_length=20, help_text='dia/mes/ano')
    status = models.BooleanField(verbose_name='Concluido', default=False)
    visto = models.BooleanField(verbose_name='Check', default=False)


class Inscricao(models.Model):
    RPT1 = [
        ('Selecione', 'Selecione'),
        ('Linguagens e Códigos', 'Linguagens e Códigos'),
        ('Ciência Exatas', 'Ciência Exatas'),
        ('Ciências Humanas', 'Ciências Humanas'),
        ('Ciências Biológicas', 'Ciências Biológicas'),
        ('Educação Física', 'Educação Física'),
        ('Professor Polivalente', 'Professor Polivalente')
    ]
    RPT2 = [
        ('Selecione', 'Selecione'),
        ('Linguagens e Códigos', 'Linguagens e Códigos'),
        ('Ciência Exatas', 'Ciência Exatas'),
        ('Ciências Humanas', 'Ciências Humanas'),
        ('Ciências Biológicas', 'Ciências Biológicas'),
        ('Educação Física', 'Educação Física'),
        ('Professor Polivalente', 'Professor Polivalente')
    ]
    RPT3 = [
        ('Selecione', 'Selecione'),
        ('Linguagens e Códigos', 'Linguagens e Códigos'),
        ('Ciência Exatas', 'Ciência Exatas'),
        ('Ciências Humanas', 'Ciências Humanas'),
        ('Ciências Biológicas', 'Ciências Biológicas'),
        ('Educação Física', 'Educação Física'),
        ('Professor Polivalente', 'Professor Polivalente')
    ]
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE)
    opcao1 = models.CharField(verbose_name='1º Opção para Ampliação', max_length=60, choices=RPT1, default='')
    opcao2 = models.CharField(verbose_name='2º Opção para Ampliação', max_length=60, choices=RPT2, default='', null=True, blank=True)
    opcao3 = models.CharField(verbose_name='3º Opção para Ampliação', max_length=60, choices=RPT3, default='', null=True, blank=True)
    nomeacao = models.FileField(upload_to='docs/nomeacoes', verbose_name='Termo de Posse', max_length=300,
                                validators=[validate_pdf_extension])
    diploma = models.FileField(upload_to='docs/nomeacao', verbose_name='Diploma', max_length=300,
                               validators=[validate_pdf_extension])
    diploma1 = models.FileField(upload_to='docs/nomeacao', verbose_name='Diploma', null=True, blank=True, help_text='Opcional',
                                max_length=300, validators=[validate_pdf_extension])
    diploma2 = models.FileField(upload_to='docs/nomeacao', verbose_name='Diploma', null=True, blank=True, help_text='Opcional',
                                max_length=300, validators=[validate_pdf_extension])
    informacoes_academicas = models.ForeignKey(InformacoesAcademicas, verbose_name='Informações Acadêmicas',
                                               on_delete=models.DO_NOTHING, null=True, blank=True)
    concurso = models.ForeignKey(Concurso, on_delete=models.DO_NOTHING,
                                 verbose_name='Informações sobre o concurso', null=True, blank=True)
    termo = models.BooleanField(verbose_name='Sim, eu aceito os termos', default=False)
    concluido = models.BooleanField(verbose_name='Concluido', default=False)
    analisado = models.BooleanField(verbose_name='Analisado', default=False)
    visto = models.BooleanField(verbose_name='Check', default=False)

    @classmethod
    def inscricoes_concluidas(cls):
        return cls.objects.filter(concluido=True)

    @classmethod
    def inscricoes_incompletas(cls):
        return cls.objects.filter(concluido=False)

    @classmethod
    def inscricoes_analisadas(cls):
        return cls.objects.filter(analisado=True)

    @classmethod
    def inscricoes_pendentes(cls):
        return cls.objects.filter(analisado=False, concluido=True)

    def __str__(self):
        return self.professor.nome

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'


class RequerimentoAmpliacao(models.Model):
    RESPOSTA = [
        ('Selecione aqui', 'Selecione aqui'),
        ('Não mpliado', 'Não ampliado'),
        ('Lotado em regência em sala de aula', 'Lotado em regência em sala de aula'),
        ('Lotado em regência em ambientes educacionais de aprendizagem '
         '(Laboratório de informática, Biblioteca, Secretaria Escolar e/outros ambientes )',
         'Lotado em regência em ambientes educacionais de aprendizagem '
         '(Laboratório de informática, Biblioteca, Secretaria Escolar e/outros ambientes )'),
        ('Afastado das funções por problemas de saúde', 'Afastado das funções por problemas de saúde'),
        ('Cedido a outras repartições', 'Cedido a outras repartições'),
        ('Em licença prêmio e/ou sem remuneração', 'Em licença prêmio e/ou sem remuneração'),
        ('Afastado das funções por outros motivos', 'Afastado das funções por outros motivos'),
        ('Exercendo cargo comissionado na esfera pública municipal',
         'Exercendo cargo comissionado na esfera pública municipal'),
    ]
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    escola = models.CharField(verbose_name='Escola', max_length=120, null=True, blank=True)
    semestre = models.CharField(verbose_name='Semestre', max_length=120, null=True, blank=True)
    cargo = models.CharField(verbose_name='Qual o cargo?', max_length=120, null=True, blank=True)
    anexo = models.FileField(upload_to='docs/nomeacao', verbose_name='Anexar ficha financeira', null=True, blank=True,
                                max_length=300, validators=[validate_pdf_extension])
    opcao = models.CharField(verbose_name='Ampliação Temporária', choices=RESPOSTA, default='', max_length=200)
    status = models.BooleanField(verbose_name='Concluido', default=False)
    requerimento_visto = models.BooleanField(verbose_name='Check', default=False)

    def __str__(self):
        return f'{self.inscricao} - {self.semestre}'



class Certificado(models.Model):
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    curso = models.CharField(verbose_name='Curso', max_length=120)
    certificado = models.FileField(upload_to='docs/certificado', verbose_name='Certificado',
                                   max_length=300, validators=[validate_pdf_extension], help_text='Permitido apenas arquivos em formato PDF.')
    certificado_visto = models.BooleanField(verbose_name='Check', default=False)

    def __str__(self):
        return self.curso


class Resultado(models.Model):
    RESULTADO = [
        ('Selecione', 'Selecione'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado')
    ]
    inscricao = models.OneToOneField(Inscricao, verbose_name='Resultado da Inscrição', on_delete=models.CASCADE)
    resultado = models.CharField(verbose_name='Resultado', max_length=30, choices=RESULTADO, default='Selecione')
    comentario = models.TextField(null=True, blank=True, verbose_name='Comentário')
