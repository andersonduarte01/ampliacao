from ..inscricao.models import Inscricao, RequerimentoAmpliacao

def corrigirRequerimento():
    inscricoes = Inscricao.objects.all()
    for inscricao in inscricoes:
        requerimentos = RequerimentoAmpliacao.objects.filter(inscricao=inscricao)
        for requerimento in requerimentos:
            if requerimento.semestre == '3º Semestre - 2021':
                requerimento.semestre = '3º Semestre - 2022'
                requerimento.save(force_update=True)
            elif requerimento.semestre == '4º Semestre - 2021':
                requerimento.semestre = '4º Semestre - 2022'
                requerimento.save(force_update=True)
            elif requerimento.semestre == '5º Semestre - 2021':
                requerimento.semestre = '5º Semestre - 2023'
                requerimento.save(force_update=True)
            elif requerimento.semestre == '6º Semestre - 2021':
                requerimento.semestre = '6º Semestre - 2023'
                requerimento.save(force_update=True)


