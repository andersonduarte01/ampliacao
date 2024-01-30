from django.db import models
from ..professor.models import Professor
from .decoradores import validate_pdf_extension


class InformacoesAcademicas(models.Model):
    RESPOSTA = [
        ('SIM', 'SIM'),
        ('NÃO', 'NÃO'),
    ]
    RESULTADO = [
        ('0', 'Selecione'),
        ('1', 'Aprovado'),
        ('2', 'Não Aprovado')
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
    info_visto = models.CharField(verbose_name='Check', max_length=15, choices=RESULTADO, default='Selecione')

    def anexoChecar(self):
        if self.anexo:
            return True
        else:
            return False

class Concurso(models.Model):
    RESULTADO = [
        ('0', 'Selecione'),
        ('1', 'Aprovado'),
        ('2', 'Não Aprovado')
    ]
    realizacao = models.CharField(verbose_name='Ano de realização do Concurso', max_length=12)
    area = models.CharField(verbose_name='Cargo do Concurso', max_length=80)
    posse = models.CharField(verbose_name='Data da posse do Concurso', max_length=20, help_text='dia/mes/ano')
    status = models.BooleanField(verbose_name='Concluido', default=False)
    concurso_visto = models.CharField(verbose_name='Check', max_length=15, choices=RESULTADO, default='Selecione')


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

    RESULTADO = [
        ('0', 'Selecione'),
        ('1', 'Aprovado'),
        ('2', 'Não Aprovado')
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
    visto = models.CharField(verbose_name='Check', max_length=15, choices=RESULTADO, default='Selecione')

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
    RESULTADO1 = [
        ('0', 'Selecione'),
        ('1', 'Aprovado'),
        ('2', 'Não Aprovado')
    ]
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    escola = models.CharField(verbose_name='Escola', max_length=120, null=True, blank=True)
    semestre = models.CharField(verbose_name='Semestre', max_length=120, null=True, blank=True)
    cargo = models.CharField(verbose_name='Qual o cargo?', max_length=120, null=True, blank=True)
    anexo = models.FileField(upload_to='docs/nomeacao', verbose_name='Anexar ficha financeira', null=True, blank=True,
                                max_length=300, validators=[validate_pdf_extension])
    opcao = models.CharField(verbose_name='Ampliação Temporária', choices=RESPOSTA, default='', max_length=200)
    status = models.BooleanField(verbose_name='Concluido', default=False)
    requerimento_visto = models.CharField(verbose_name='Check', max_length=15, choices=RESULTADO1, default='Selecione')

    def __str__(self):
        return f'{self.inscricao} - {self.semestre}'


class Certificado(models.Model):
    RESULTADO = [
        ('0', 'Selecione'),
        ('1', 'Aprovado'),
        ('2', 'Não Aprovado')
    ]
    PONTUACAO = [
        (0, '0'),
        (0.5, '0.5'),
    ]
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    curso = models.CharField(verbose_name='Curso', max_length=120)
    certificado = models.FileField(upload_to='docs/certificado', verbose_name='Certificado',
                                   max_length=300, validators=[validate_pdf_extension], help_text='Permitido apenas arquivos em formato PDF.')
    certificado_visto = models.CharField(verbose_name='Check', max_length=15, choices=RESULTADO, default='Selecione')
    pontuacao = models.DecimalField(verbose_name='Pontuação',max_digits=2, decimal_places=1, choices=PONTUACAO, default=0)

    def __str__(self):
        return self.curso


class TotalPontos(models.Model):
    PONTOS_CHOICES = [
        (0.0, '0.0'),
        (0.5, '0.5'),
        (1.0, '1.0'),
        (1.5, '1.5'),
        (2.0, '2.0'),
        (2.5, '2.5'),
        (3.0, '3.0'),
    ]
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    total_pontos = models.DecimalField(max_digits=3, decimal_places=1, default=0, choices=PONTOS_CHOICES)

    def __str__(self):
        return self.total_pontos


class PosTotalPontos(models.Model):
    PONTOS_GRADUACAO = [
        (0.0, '0.0'),
        (0.5, '0.5'),
        (1.0, '1.0'),
        (1.5, '1.5'),
        (2.0, '2.0'),
        (2.5, '2.5'),
        (3.0, '3.0'),
    ]
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    pos_pontos = models.DecimalField(max_digits=3, decimal_places=1, default=0, choices=PONTOS_GRADUACAO)

class Resultado(models.Model):
    RESULTADO = [
        ('', 'Selecione'),
        ('Aprovado', 'Aprovado'),
        ('Negado', 'Negado')
    ]
    inscricao = models.OneToOneField(Inscricao, verbose_name='Resultado da Inscrição', on_delete=models.CASCADE)
    resultado = models.CharField(verbose_name='Resultado', max_length=30, choices=RESULTADO, default='Selecione')
    comentario = models.TextField(null=True, blank=True, verbose_name='Comentário')


class AmpliacaoComplemento(models.Model):
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
    RESULTADO1 = [
        ('0', 'Selecione'),
        ('1', 'Aprovado'),
        ('2', 'Não Aprovado')
    ]
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    escola = models.CharField(verbose_name='Escola', max_length=120, null=True, blank=True)
    semestre = models.CharField(verbose_name='Semestre', max_length=120, null=True, blank=True)
    cargo = models.CharField(verbose_name='Qual o cargo?', max_length=120, null=True, blank=True)
    anexo = models.FileField(upload_to='docs/nomeacao', verbose_name='Anexar ficha financeira', null=True, blank=True,
                                max_length=300, validators=[validate_pdf_extension])
    opcao = models.CharField(verbose_name='Ampliação Temporária', choices=RESPOSTA, default='', max_length=200)
    status = models.BooleanField(verbose_name='Concluido', default=False)
    complemento_visto = models.CharField(verbose_name='Check', max_length=15, choices=RESULTADO1, default='Selecione')

    def __str__(self):
        return f'{self.inscricao}'


class Experiencia(models.Model):
    VALORES_CHOICES = [
        ('0', '0.0'),
        ('0.2', '0.2'),
        ('0.4', '0.4'),
        ('0.6', '0.6'),
        ('0.8', '0.8'),
        ('1.0', '1.0'),
        ('1.2', '1.2'),
        ('1.4', '1.4'),
        ('1.6', '1.6'),
        ('1.8', '1.8'),
        ('2.0', '2.0'),
    ]
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    anos_experiencia = models.CharField(verbose_name='Experiência', max_length=10, default='0')
    pontos_experiencia = models.CharField(max_length=3, choices=VALORES_CHOICES, default=0.0,)

    def __str__(self):
        return self.pontos_experiencia


class Documento(models.Model):
    documento = models.FileField(upload_to='docs/certificado', verbose_name='Documento',
                                        max_length=300, validators=[validate_pdf_extension],
                                        help_text='Permitido apenas arquivos em formato PDF.')

# class Certificado(models.Model):
#     inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
#     razoes = models.TextField(verbose_name='Razões do Recurso')
#     recurso = models.FileField(upload_to='docs/certificado', verbose_name='Certificado',
#                                    max_length=300, validators=[validate_pdf_extension],
#                                    help_text='Permitido apenas arquivos em formato PDF.')
#     recurso_visto = models.BooleanField(verbose_name='Analisado?', default=False)
#
#     def __str__(self):
#         return self.curso