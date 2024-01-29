from ..inscricao.models import Resultado

def atualize_ja():
    resultados = Resultado.objects.all()
    for results in resultados:
        print(results.resultado)
        if results.resultado == 'Aprovado':
            results.comentario = f'Do exame da documentação acostada pelo(a) requerente {results.inscricao.professor}, Matrícula {results.inscricao.professor.matricula}, verificou-se o preenchimento dos requisitos previstos na Lei Municipal Nº 829/2023 e no EDITAL N° 005/2023 – Processo de Ampliação Definitiva de Carga Horária de Trabalho dos Professores Efetivos do Município de Pedra Branca-CE; ensejando, portanto, a APROVAÇÃO do(a) candidato(a) no certame, observada sua colocação na lista de classificação.'
            results.save(force_update=True)
        elif results.resultado == 'Negado':
            results.comentario = f'Do exame da documentação acostada pelo(a) requerente {results.inscricao.professor}, Matrícula {results.inscricao.professor.matricula}, verificou-se o NÃO preenchimento dos requisitos previstos no(s) __(espaço)____, da Lei Municipal Nº 829/2023 e do EDITAL N° 005/2023 – Processo de Ampliação Definitiva de Carga Horária de Trabalho dos Professores Efetivos do Município de Pedra Branca-CE, em virtude de não ter comprovado a condição de (ESPAÇO A SER PREENCHIDO), ensejando, portanto, a NÃO aprovação do(a) candidato(a) no certame.'
            results.save(force_update=True)
